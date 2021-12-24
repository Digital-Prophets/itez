import datetime

from django.conf import settings

from fpdf import FPDF, HTMLMixin

from itez.beneficiary.models import Beneficiary, MedicalRecord


date_today = datetime.date.today().strftime("%b %d %Y")


class PDF(FPDF, HTMLMixin):
    def __init__(self, *args, beneficiary_obj=None, medical_records=None, **kwargs) -> None:
        self.beneficiary_obj = beneficiary_obj
        self.medical_records = medical_records
        super().__init__(*args, **kwargs)

    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        # set font
        self.set_font("helvetica", "I", 8)
        # Set font color grey
        self.set_text_color(169, 169, 169)
        # Page number
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


    def print_header(self, height, title, font_size):
        self.set_font("helvetica", "B", font_size)

        self.set_y(height)
        self.cell(70, 8, title, ln=1)

    def beneficiary_info_to_dict(self):
        beneficiary_data = {
            "Name": f"{self.beneficiary_obj.first_name} {self.beneficiary_obj.last_name}",
            "Gender": self.beneficiary_obj.gender,
            "Sex": self.beneficiary_obj.sex,
            "Phone Number": self.beneficiary_obj.phone_number,
            "Email": self.beneficiary_obj.email,
            "Date of Birth": self.beneficiary_obj.date_of_birth,
            "Marital Status": self.beneficiary_obj.marital_status,
            "Address": self.beneficiary_obj.address,
            "ART Status": self.beneficiary_obj.art_status,
            "HIV Status": self.beneficiary_obj.hiv_status,
            "Registered Facility": self.beneficiary_obj.registered_facility,
            "Name of Spouse": self.beneficiary_obj.name_of_spouse,
            "Number of Children": self.beneficiary_obj.number_of_children,
            "Number of Siblings": self.beneficiary_obj.number_of_siblings,
            "Education Leval": self.beneficiary_obj.education_level,
            "Alive": self.beneficiary_obj.alive,
        }
        return beneficiary_data

    def beneficiary_details(self):
        self.add_page()

        self.image("/app/itez/static/assets/moh_logo.png", 170, 8, 25)
        self.set_font("helvetica", "B", 16)

        self.print_header(35, f"Medical Record For: {self.beneficiary_obj.first_name} {self.beneficiary_obj.last_name}", 18)

        self.set_font("helvetica", "B", 13)
        self.cell(70, 8, f"Date: {date_today}", ln=1)
        self.line(10, 58, 200, 58)

        self.print_header(62, "Beneficiary Details", 14)
        self.set_font("helvetica", "", 11)

        self.set_y(70)
        row_count = 1
        y_axis = 70
        for field_name, value in self.beneficiary_info_to_dict().items():
            if not value:
                continue
            # self.set_y(50)
            if row_count >= 9:
                self.set_y(y_axis)
                self.set_x(86)
                self.cell(60, 8, f"{field_name}: {value}", ln=1)
                row_count += 1
                y_axis += 9.5
            else:
                if field_name == "Address":
                    self.multi_cell(60, 8, f"{field_name}: {value}")
                else:
                    self.cell(60, 8, f"{field_name}: {value}", ln=1)
                row_count += 1
        self.set_y(220)
        self.set_x(45)
        self.set_font("helvetica", "B", 12)
        self.cell(60, 8, f"Approved By: ", ln=1, align='C')
        self.image(f"{self.beneficiary_obj.profile_photo.path}", 155, 85, 50)
        self.line(60, 230, 130, 230)

    def print_footer(self, beneficiary_id):
        self.set_y(-35)
        self.cell(60, 8, f"Beneficiary ID: {beneficiary_id}")
        self.set_x(150)
        self.cell(60, 8, f"Ministry of Health Zambia")


    def print_medical_record_details(self, table_data):
        line_height = self.font_size * 2.5
        col_width = self.epw / 4  # distribute content evenly
        self.set_y(120)
        for row_num, row_data in enumerate(table_data):
            if row_num == 0:
                self.set_font("helvetica", "B", line_height)
            else:
                self.set_font("helvetica", "", line_height)
            if len(row_data[1]) > 70 or len(row_data[4]) > 70:
                for index, datum in enumerate(row_data):
                    if index == 0:
                        self.multi_cell(
                            col_width - 20,
                            line_height + 5,
                            datum,
                            border=1,
                            ln=3,
                            max_line_height=self.font_size,
                        )

                    elif index == 2:
                        self.multi_cell(
                            col_width - 30,
                            line_height + 5,
                            datum,
                            border=1,
                            ln=3,
                            max_line_height=self.font_size,
                        )
                    else:
                        self.multi_cell(
                        col_width,
                        line_height + 5,
                        datum,
                        border=1,
                        ln=3,
                        max_line_height=self.font_size,
                    )
                self.ln(line_height)
            else:
                for index, datum in enumerate(row_data):
                    if index == 0:
                        self.multi_cell(
                            col_width - 20,
                            line_height,
                            datum,
                            border=1,
                            ln=3,
                            max_line_height=self.font_size,
                        )

                    elif index == 2:
                        self.multi_cell(
                            col_width - 30,
                            line_height,
                            datum,
                            border=1,
                            ln=3,
                            max_line_height=self.font_size,
                        )
                    else:
                        self.multi_cell(
                        col_width,
                        line_height,
                        datum,
                        border=1,
                        ln=3,
                        max_line_height=self.font_size,
                    )
                self.ln(line_height)


    def print_records(self):
        for record in self.medical_records:
            service_personnel_name = (
                record.service.service_personnel.first_name
                + " "
                + record.service.service_personnel.last_name
            )
            self.add_page()

            self.print_header(
                35, f"Medical Record Entry as of: {record.created.strftime('%b %d %Y')}", 18
            )
            self.line(10, 45, 200, 45)


            self.set_y(80)
            self.set_font("helvetica", "B", 11)
            self.cell(60, 8, f"Service Facility: {record.service_facility.name}", ln=1)
            self.cell(60, 8, f"Service Name: {record.service.title}", ln=1)
            self.set_y(79)
            self.set_x(110)
            self.cell(60, 8, f"Provider Personel: {service_personnel_name}", ln=1)
            self.set_y(89)
            self.set_x(110)
            self.multi_cell(90, 8, f"Comments: {record.provider_comments}", ln=1)

            TABLE_HEADERS = [
                    "Interraction Date",
                    "Prescription",
                    "No. of Days",
                    "When to take ",
                    "Lab comment",
                ]

            table_data = [
                TABLE_HEADERS,
            ]
            table_data.append([record.interaction_date.strftime("%d %b %Y"), record.prescription, str(record.no_of_days), record.when_to_take, record.lab])
            self.print_medical_record_details(table_data)


def create_document(filename):
    beneficiary_obj = Beneficiary.objects.get(id=1)
    medical_records = MedicalRecord.objects.filter(beneficiary__id=beneficiary_obj.id)

    # Create a self object
    pdf = PDF("P", "mm", "A4", beneficiary_obj=beneficiary_obj, medical_records=medical_records)

    # get total page numbers
    pdf.alias_nb_pages()

    # Set auto page break
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.beneficiary_details()
    pdf.print_footer(beneficiary_obj.beneficiary_id)

    pdf.print_records()
    pdf.output(filename)



# import datetime
# import os

# import io
# from django.conf import settings

# from reportlab.platypus import (
#     SimpleDocTemplate,
#     Paragraph,
#     Spacer,
#     Table,
#     TableStyle,
#     Frame,
#     PageTemplate,
#     NextPageTemplate,
#     flowables,
# )

# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.rl_config import defaultPageSize
# from reportlab.lib.units import inch, cm
# from reportlab.lib import colors
# from reportlab.pdfbase.ttfonts import TTFont, TTFError
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfgen import canvas

# from itez.beneficiary.models import Beneficiary, MedicalRecord


# media_root = settings.MEDIA_ROOT
# static_root = settings.STATIC_ROOT
# date_today = datetime.date.today().strftime("%b %d %Y")


# PAGE_HEIGHT = defaultPageSize[1]
# PAGE_WIDTH = defaultPageSize[0]

# styles = getSampleStyleSheet()


# def create_pdf(filename, beneficiary_obj, medical_records):
#     doc = SimpleDocTemplate(filename)
#     Story = []
#     for i in range(50):
#         Story.append(Spacer(1, 0.2 * inch))

#     def get_font():
#         """
#         Set the fonts for the document.
#         """
#         try:
#             font_folder = os.path.join(static_root, "assets/fonts", "Roboto")
#             bold_ttf_file = os.path.join(font_folder, "Roboto-Bold.ttf")
#             regular_ttf_file = os.path.join(font_folder, "Roboto-Regular.ttf")
#             pdfmetrics.registerFont(TTFont("Roboto-Bold", bold_ttf_file))
#             pdfmetrics.registerFont(TTFont("Roboto-Regular", regular_ttf_file))
#         except (TTFError, KeyError):
#             pass


#     def draw_string(canvas, x=0, y=0, text=""):
#         """
#         Draws text on the document.
#         """
#         canvas.drawString(x, y, text)


#     def draw_line(canvas, x1=0, y1=0, x2=0, y2=0):
#         """
#         Draws a line on the document.
#         """
#         canvas.line(x1, y1, x2, y2)


#     def draw_photo(canvas, photo_path, x=0, y=0, width=0, height=0):
#         """
#         Draws an image on the document.
#         """
#         canvas.drawImage(
#             photo_path,
#             x,
#             y,
#             height=height,
#             width=width,
#             preserveAspectRatio=True,
#             anchor="c",
#             mask="auto",
#         )


#     def beneficiary_obj_to_dict():
#         """
#         Converts the beneficary model object into a dict and returns a dict containing only
#         the required fields and thier corresponsing values. This allows the data to be easily
#         iterated over and rendered dynamically.
#         """

#         beneficiary_data = {
#             "Name": f"{beneficiary_obj.first_name} {beneficiary_obj.last_name}",
#             "Gender": beneficiary_obj.gender,
#             "Sex": beneficiary_obj.sex,
#             "Phone Number": beneficiary_obj.phone_number,
#             "Email": beneficiary_obj.email,
#             "ART Status": beneficiary_obj.art_status,
#             "Last VL": beneficiary_obj.last_vl,
#             "HIV Status": beneficiary_obj.hiv_status,
#             "Registered Facility": beneficiary_obj.registered_facility,
#             "Date of Birth": beneficiary_obj.date_of_birth,
#             "Marital Status": beneficiary_obj.marital_status,
#             "Name of Spouse": beneficiary_obj.name_of_spouse,
#             "Number of Children": beneficiary_obj.number_of_children,
#             "Number of Siblings": beneficiary_obj.number_of_siblings,
#             "Parent Details": beneficiary_obj.parent_details,
#             "Education Leval": beneficiary_obj.education_level,
#             "Address": beneficiary_obj.address,
#             "Alive": "Yes" if beneficiary_obj.alive else "No",
#         }
#         return beneficiary_data


#     def draw_beneficiary_info(canvas, doc):
#         """
#         Draws all the beneficiary meta data on the document.
#         """
#         canvas.setFillColorRGB(0, 0, 0)
#         canvas.setFont("Roboto-Regular", 12)

#         height_count = 100

#         data = beneficiary_obj_to_dict()

#         for field_name, value in data.items():
#             if not value:
#                 continue  # Do not draw the value if its None
#             draw_string(
#                 canvas,
#                 x=doc.leftMargin,
#                 y=doc.height - height_count,
#                 text=f"{field_name}: {value}",
#             )
#             height_count += 20


#     def get_profile_photo():
#         if beneficiary_obj.profile_photo:
#             return beneficiary_obj.profile_photo.path
#         elif beneficiary_obj.gender == "Male":
#             return f"{static_root}/assets/images/faces/male.jpeg"
#         elif beneficiary_obj.gender == "Female":
#             return f"{static_root}/assets/images/faces/female.jpeg"
#         else:
#             return f"{static_root}/assets/images/faces/dummy_profile.jpeg"


#     def myFirstPage(canvas, doc):
#         get_font()

#         canvas.saveState()

#         canvas.setFont("Roboto-Regular", 12)

#         draw_photo(
#             canvas,
#             f"{static_root}/assets/moh_logo.png",
#             x=(doc.rightMargin + 450),
#             y=(doc.height + 60),
#             height=70,
#             width=70,
#         )

#         canvas.setFont("Roboto-Bold", 15)
#         draw_string(
#             canvas,
#             x=doc.leftMargin,
#             y=doc.height - 10,
#             text=f"Medical Record History For: {beneficiary_obj.first_name} {beneficiary_obj.last_name} ",
#         )

#         canvas.setFont("Roboto-Regular", 12)
#         draw_string(
#             canvas,
#             x=doc.leftMargin,
#             y=doc.height - 30,
#             text=f"Date: {date_today}",
#         )

#         photo_path = get_profile_photo()
#         draw_photo(
#             canvas,
#             photo_path,
#             x=doc.rightMargin + 360,
#             y=(doc.height - 260),
#             height=150,
#             width=150,
#         )

#         draw_line(canvas, x1=doc.leftMargin, y1=650, x2=doc.rightMargin + 440, y2=650)

#         canvas.setFont("Roboto-Bold", 13)
#         draw_string(canvas, x=doc.leftMargin, y=doc.height - 80, text="Beneficiary Details")

#         draw_beneficiary_info(canvas, doc)

#         # Draws Beneficiary ID
#         canvas.setFont("Roboto-Regular", 12)
#         draw_string(
#             canvas,
#             x=doc.leftMargin,
#             y=doc.height - 650,
#             text=f"ID: {beneficiary_obj.beneficiary_id}",
#         )
#         draw_string(
#             canvas,
#             x=doc.rightMargin + 340,
#             y=doc.height - 650,
#             text="Ministry of Health Zambia",
#         )

#         draw_line(canvas, x1=doc.leftMargin, y1=330, x2=doc.rightMargin + 440, y2=330)

#         draw_string(
#             canvas,
#             x=doc.rightMargin + 150,
#             y=doc.height - 530,
#             text="Approved By: Senior Doctor James",
#         )
#         draw_line(canvas, x1=doc.leftMargin + 150, y1=150, x2=doc.rightMargin + 330, y2=150)

#         canvas.setFont("Roboto-Regular", 8)

#         canvas.restoreState()


#     def myLaterPages(canvas, doc):
#         canvas.saveState()
#         canvas.setFont("Roboto-Bold", 16)

#         styleN = styles["BodyText"]
#         for record in medical_records:
#             # canvas.saveState
#             draw_line(canvas, x1=doc.leftMargin, y1=740, x2=doc.rightMargin + 440, y2=740)

#             service_personnel_name = (
#                 record.service.service_personnel.first_name
#                 + " "
#                 + record.service.service_personnel.last_name
#             )

#             draw_string(
#                 canvas,
#                 x=doc.leftMargin,
#                 y=doc.height,
#                 text=f"Medical Record Entry as of: {record.created.strftime('%b %d %Y')}",
#             )

#             canvas.setFont("Roboto-Bold", 14)
#             # draw_string(
#             #     canvas,
#             #     x=doc.leftMargin,
#             #     y=doc.height - 20,
#             #     text=f"Service Facility: {record.service_facility.name}",
#             # )
#             P = Paragraph(f"Service Facility: {record.service_facility.name}")
#             P.wrapOn(canvas, 200, 20)
#             P.drawOn(canvas, doc.leftMargin, doc.height - 20)

#             P2 = Paragraph(
#                 f"Service Name: {record.service.title} mv mjhhfnc j,kl k,kvk jjmfvc  jgcm hjffcg kj hk hk hkvcxfh      gvvvgj",
#                 styleN,
#             )
#             P2.wrapOn(canvas, 200, 100)
#             P2.drawOn(canvas, doc.leftMargin, doc.height - 70)

#             s = Spacer(1, 0.2 * inch)

#             P3 = Paragraph(f"Provider Personnel: {service_personnel_name}")
#             P3.wrapOn(canvas, 200, 40)
#             P3.drawOn(canvas, doc.rightMargin + 200, doc.height - 20)

#             P4 = Paragraph(f"Comments: {record.provider_comments}")
#             P4.wrapOn(canvas, 200, 40)
#             P4.drawOn(canvas, doc.rightMargin + 200, doc.height - 70)

#             s = Spacer(1, 0.2 * inch)

#             styleN = styles["BodyText"]

#             table = [
#                 [
#                     Paragraph("Interraction Date", styleN),
#                     Paragraph("Prescription", styleN),
#                     Paragraph("No. Days", styleN),
#                     Paragraph("When to take", styleN),
#                     Paragraph("Lab comments", styleN),
#                 ],
#                 [
#                     Paragraph(
#                         record.interaction_date.strftime("%b %d %Y %H:%M:%S") + "", styleN
#                     ),
#                     Paragraph(
#                         record.prescription,
#                         styleN,
#                     ),
#                     Paragraph(str(record.no_of_days), styleN),
#                     Paragraph(record.when_to_take, styleN),
#                     Paragraph(str(record.lab), styleN),
#                 ],
#             ]

#             # for medical_record in medical_records:
#             #     service_personnel_name = (
#             #         medical_record.service.service_personnel.first_name
#             #         + " "
#             #         + medical_record.service.service_personnel.last_name
#             #     )
#             #     table.append(
#             #         [
#             #             Paragraph(medical_record.service.title),
#             #             Paragraph(service_personnel_name),
#             #             Paragraph(medical_record.provider_comments),
#             #             Paragraph(medical_record.service_facility.name),
#             #         ]
#             #     )

#             t = Table(
#                 table,
#                 repeatRows=1,
#                 colWidths=[100, 100, 55, 60, 100],
#                 style=TableStyle(
#                     [
#                         ("GRID", (0, 0), (-1, -1), 1.0, colors.gray),
#                         # ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
#                         # ("BOX", (0, 0), (1, 0), 1.0, colors.black),
#                     ]
#                 ),
#             )

#             t.wrapOn(canvas, 300, 300)
#             t.drawOn(canvas, doc.leftMargin, doc.height - 200)

#             # draw_string(
#             #     canvas,
#             #     x=doc.leftMargin,
#             #     y=doc.height - 40,
#             #     text=f"Service Name: {record.service.title}",
#             # )

#             # draw_string(
#             #     canvas,
#             #     x=doc.rightMargin + 200,
#             #     y=doc.height - 20,
#             #     text=f"Provider Personel: {service_personnel_name}",
#             # )

#             # draw_string(
#             #     canvas,
#             #     x=doc.rightMargin + 200,
#             #     y=doc.height - 40,
#             #     text=f"Comments: {record.provider_comments}",
#             # )
#             # pass
#             # canvas.restoreState()
#         canvas.restoreState()

#     doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)




