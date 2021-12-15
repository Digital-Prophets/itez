import os
from datetime import datetime

from django.conf import settings

from celery import shared_task

from config import celery_app

from .models import Beneficiary, MedicalRecord
from .resources import BeneficiaryResource
from .utils import GenerateMedicalReport


@shared_task(bind=True)
def generate_export_file(self):
    """
    This task generates a file containing all Beneficiary data for export, stores for file temporary, and return
    the filename to be used to construct a full download URL for the file on the client.
    """
    beneficiary_resource = BeneficiaryResource()
    dataset = beneficiary_resource.export()
    filename = save_exported_data(data=dataset.xlsx, file_ext='.xlsx')
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
    directory = f"{settings.MEDIA_ROOT}/beneficiary_report"

    
    if not os.path.exists(directory):
        os.mkdir(directory)

    timestamp = datetime.now().strftime("%H_%M_%S_%f")
    filename = f"{beneficiary_obj.beneficiary_id}_{timestamp}.pdf"
    full_filepath = os.path.join(directory, filename)

    GenerateMedicalReport(full_filepath, beneficiary_obj, medical_records)

    return {"TASK_TYPE": "GENERATE_MEDICAL_REPORT", "RESULT": filename}