import uuid
import os
import shutil

from django.conf import settings
from django.forms.models import model_to_dict

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    NextPageTemplate,
    Table,
    TableStyle,
    Paragraph,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from .resources import BeneficiaryResource


def generate_uuid():
    """
    Generates a seven digit agent ID and a unique ID.
    """
    unique_id = uuid.uuid4()
    agent_code = f"Agent-{str(unique_id)[1:8].upper()}"
    beneficiary_code = f"Beneficiary-{str(unique_id)[1:8].upper()}"

    return beneficiary_code, agent_code


def zip_directory(archive_name=None, format=None, directory=None):
    shutil.make_archive(archive_name, format, directory)
