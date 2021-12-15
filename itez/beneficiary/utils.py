import uuid
import os

from django.conf import settings

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, Table, TableStyle, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from .resources import BeneficiaryResource


beneficiary_resource = BeneficiaryResource()
dataset = beneficiary_resource.export()


def generate_uuid():
    """
    Generates a seven digit agent ID and a unique ID.
    """
    unique_id = uuid.uuid4()
    agent_code = f"Agent-{str(unique_id)[1:8].upper()}"
    beneficiary_code = f"Beneficiary-{str(unique_id)[1:8].upper()}"
    
    return beneficiary_code, agent_code


class GenerateMedicalReport(BaseDocTemplate):

    def __init__(self, filename, beneficiary_obj, medical_records, **kwargs):
        super().__init__(filename, page_size=A4, _pageBreakQuick=0, **kwargs)
        self.leftMargin = self.leftMargin - 22
        self.rightMargin = self.leftMargin + 495
        self.media_root = settings.MEDIA_ROOT
        self.static_root = settings.STATIC_ROOT
        self.beneficiary_obj = beneficiary_obj
        self.medical_records = medical_records

        self.page_width = (self.width + self.leftMargin * 2)
        self.page_height = (self.height + self.bottomMargin * 2)


        styles = getSampleStyleSheet()

        # Setting up the frames, frames are use for dynamic content not fixed page elements
        first_page_table_frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height - 15 * cm, id='small_table')
        later_pages_table_frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='large_table')

        # table_frame = Frame(self.leftMargin, self.bottomMargin + 5, self.width, self.height, id='large_table')
        # t_frame = Frame(self.leftMargin, self.bottomMargin + 5, self.width, self.height - 6 * cm)
        # Creating the page templates
        first_page = PageTemplate(id='FirstPage', frames=[first_page_table_frame], onPage=self.first_page)
        later_pages = PageTemplate(id='LaterPages', frames=[later_pages_table_frame], onPage=self.add_default_info)
        self.addPageTemplates([first_page, later_pages])

        # Tell Reportlab to use the other template on the later pages,
        # by the default the first template that was added is used for the first page.
        story = [NextPageTemplate(['*', 'LaterPages'])]

        story.append(
            Table(self._create_table(),
            repeatRows=1,
                style=TableStyle(
                        [
                            ('GRID',(0,0),(-1,-1), 1.0, colors.gray),
                            ('BOX', (0,0), (-1,-1), 1.0, colors.black),
                            ('BOX', (0,0), (1,0), 1.0, colors.black),
                        ]
                    )
                )
            )


        self.build(story)

    def first_page(self, canvas, doc):
        self._get_font()
        canvas.saveState()

        # Add the Beneficiary Details and other default stuff
        self.add_default_info(canvas, doc)

        canvas.setFont('Roboto-Bold', 16)
        self._draw_string(canvas, x=self.leftMargin, y=self.height + 10, text='Beneficiary Information')
        self._draw_photo(
            canvas,
            f'{self.static_root}/assets/moh_logo.png', x=(self.rightMargin - 100), y=(self.height + 30), height=100, width=100
        )

        
        self._draw_photo(canvas, self.beneficiary_obj.profile_photo.path, x=self.rightMargin - 200, y=(self.height - 200), height=150, width=150)

        
        self._draw_line(canvas, x1=self.leftMargin , y1=670, x2=self.rightMargin, y2=670)

        self._draw_beneficiary_info(canvas, doc)
        
        self._draw_line(canvas, x1=self.leftMargin, y1=390, x2=self.rightMargin, y2=390)

        canvas.setFont('Roboto-Bold', 16)
        self._draw_string(canvas, x=self.leftMargin, y=self.height - 340, text='Medical Record')

        canvas.restoreState()

    def add_default_info(self, canvas, doc):
        canvas.saveState()

        self._create_table()


        canvas.setFont('Roboto-Regular', 12)


        # Draws Beneficiary ID
        canvas.setFont('Roboto-Regular', 14)
        self._draw_string(canvas, x=doc.leftMargin, y=self.height - 650, text=f'ID: {self.beneficiary_obj.beneficiary_id}')
        canvas.setFont('Roboto-Regular', 8)

        canvas.restoreState()

    def _get_font(self):
        try:
            font_folder = os.path.join(self.static_root,
                'assets/fonts', 'Roboto')
            bold_ttf_file = os.path.join(
                font_folder, 'Roboto-Bold.ttf')
            regular_ttf_file = os.path.join(
                font_folder, 'Roboto-Regular.ttf')
            pdfmetrics.registerFont(TTFont('Roboto-Bold', bold_ttf_file))
            pdfmetrics.registerFont(TTFont('Roboto-Regular', regular_ttf_file))
        except (TTFError, KeyError):
            pass

    def _draw_beneficiary_info(self, canvas, doc):
        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont('Roboto-Bold', 12)
        canvas.drawString(self.leftMargin, self.height - 50, f'Name: {self.beneficiary_obj.first_name} {self.beneficiary_obj.last_name}')
        canvas.drawString(self.leftMargin, self.height - 70, f'Phone No: {self.beneficiary_obj.phone_number}')
        canvas.drawString(self.leftMargin, self.height - 90, f'Address: {self.beneficiary_obj.address}')
        canvas.drawString(self.leftMargin, self.height - 110, f'Birth Date: {self.beneficiary_obj.date_of_birth}')
        canvas.drawString(self.leftMargin, self.height - 130, f'Gender: {self.beneficiary_obj.gender}')
        canvas.drawString(self.leftMargin, self.height - 150, f'HIV Status: {self.beneficiary_obj.hiv_status}')
        canvas.drawString(self.leftMargin, self.height - 170, f'ART Status: {self.beneficiary_obj.art_status}')
        canvas.drawString(self.leftMargin, self.height - 190, f'Last VL: {self.beneficiary_obj.last_vl}')

        canvas.drawString(self.leftMargin, self.height - 210, f'Education Level: {self.beneficiary_obj.education_level}')
        canvas.drawString(self.leftMargin, self.height - 230, f'Marital Status: {self.beneficiary_obj.marital_status}')
        canvas.drawString(self.leftMargin, self.height - 250, f'Spouse Name: {self.beneficiary_obj.name_of_spouse}')
        canvas.drawString(self.leftMargin, self.height - 270, f'Number of Children: {self.beneficiary_obj.number_of_children}')
        canvas.drawString(self.leftMargin, self.height - 290, f'Number of Siblings: {self.beneficiary_obj.number_of_siblings}')
    
    def _draw_string(self, canvas, x=0, y=0, text=''):
        canvas.drawString(x, y, text)

    def _draw_line(self, canvas, x1=0, y1=0, x2=0, y2=0):
        canvas.line( x1, y1, x2, y2)

    def _draw_photo(self, canvas, photo_path, x=0, y=0, width=0, height=0):
        canvas.drawImage(
            photo_path, x, y, height=height, width=width,
            preserveAspectRatio=True, anchor='c', mask='auto'
        )
    def _create_table(self):
        table = [
            ['Service Name', 'Provider Personnel', 'Comments', 'Facility'],
        ]

        for medical_record in self.medical_records:            
            service_personnel_name = medical_record.service.service_personnel.first_name + " " + medical_record.service.service_personnel.last_name
            table.append([Paragraph(medical_record.service.title), Paragraph(service_personnel_name), Paragraph(medical_record.provider_comments), Paragraph(medical_record.service_facility.name)])
        return table

