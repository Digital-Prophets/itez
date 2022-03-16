import os
import shutil
from datetime import datetime

from django.conf import settings

from celery import shared_task

from config import celery_app

from itez.beneficiary.models import Beneficiary, MedicalRecord
from itez.beneficiary.resources import BeneficiaryResource
from itez.beneficiary.pdf_utils import create_document
from itez.beneficiary.utils import zip_directory


@shared_task(bind=True)
def generate_export_file(self):
    """
    This task generates a file containing all Beneficiary data for export, stores for file temporary, and return
    the filename to be used to construct a full download URL for the file on the client.
    """
    beneficiary_resource = BeneficiaryResource()
    dataset = beneficiary_resource.export()
    filename = save_exported_data(data=dataset.xlsx, file_ext=".xlsx")
    return {"TASK_TYPE": "EXPORT_BENEFICIARY_DATA", "RESULT": filename}


def save_exported_data(data=None, file_ext=None):
    timestamp = datetime.now().strftime("%H_%M_%S_%f")
    file_export_path = f"{settings.MEDIA_ROOT}/exports"

    filename = f"all_beneficiaries_export_{timestamp}{file_ext}"

    if not os.path.exists(file_export_path):
        os.mkdir(file_export_path)

    with open(f"{file_export_path}/{filename}", "wb") as f:
        f.write(data)
        return filename


@celery_app.task()
def generate_medical_report(id):
    beneficiary_obj = Beneficiary.objects.get(id=id)
    medical_records = MedicalRecord.objects.filter(beneficiary__id=beneficiary_obj.id)

    timestamp = datetime.now().strftime("%H_%M_%S_%f")
    # Create a unique for the pdf to be created
    filename = f"{beneficiary_obj.beneficiary_id}_{timestamp}"
    # A directory where the created zipfile will be saved
    
    temporary_dir = f"{settings.MEDIA_ROOT}/temp/"
    destination_dir = f"{temporary_dir}{beneficiary_obj.beneficiary_id}{timestamp}"
    if not os.path.exists(temporary_dir):
        os.makedirs(temporary_dir)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)


    create_document(
        f"{destination_dir}/{filename}.pdf", beneficiary_obj, medical_records
    )
    for medical_record in medical_records:
        shutil.copy(medical_record.documents.path, destination_dir),

    # create zip file of medical record pdf and suppporting documents
    archive_format = "zip"
    zip_directory(
        archive_name=f"{temporary_dir}/{filename}",
        format=archive_format,
        directory=destination_dir,
    )

    shutil.rmtree(destination_dir)

    return {"TASK_TYPE": "GENERATE_MEDICAL_REPORT", "RESULT": f"{filename}.zip"}


@celery_app.task()
def delete_temporary_files(directory):
    try:
        shutil.rmtree(directory)
        return f"The directory {directory} was deleted."
    except FileNotFoundError as err:
        print(err)
