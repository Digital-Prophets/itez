# Generated by Django 3.1.13 on 2021-11-22 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("beneficiary", "0010_auto_20211122_0730"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserWorkDetail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="Company Name"
                    ),
                ),
                (
                    "work_address",
                    models.TextField(
                        blank=True, null=True, verbose_name="Work Address"
                    ),
                ),
                (
                    "company_phone",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="Company Phone number",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_work_detail",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "birth_date",
                    models.DateField(blank=True, null=True, verbose_name="Birth"),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Transgender", "Transgender"),
                            ("Other", "Other"),
                        ],
                        max_length=100,
                        null=True,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        blank=True,
                        choices=[("Male", "Male"), ("Female", "Female")],
                        max_length=100,
                        null=True,
                        verbose_name="Sex",
                    ),
                ),
                (
                    "about_me",
                    models.CharField(
                        blank=True, max_length=300, null=True, verbose_name="About Me"
                    ),
                ),
                (
                    "education_level",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("none", "None"),
                            ("primary", "Primary"),
                            ("basic", "Basic"),
                            ("secondary", "Secondary O'Level"),
                            ("certificate", "Certificate"),
                            ("diploma", "Diploma"),
                            ("degree", "Degree"),
                            ("masters", "Masters"),
                            ("doctrate", "Doctrate"),
                            ("phd", "PHD"),
                        ],
                        max_length=200,
                        null=True,
                        verbose_name="Education Level",
                    ),
                ),
                (
                    "profile_photo",
                    imagekit.models.fields.ProcessedImageField(
                        blank=True, null=True, upload_to="profile_photo"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        verbose_name="Phone Number",
                    ),
                ),
                (
                    "phone_number_2",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        verbose_name="Phone Number 2",
                    ),
                ),
                (
                    "address",
                    models.TextField(
                        blank=True, max_length=300, null=True, verbose_name="Address"
                    ),
                ),
                (
                    "postal_code",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Postal Code",
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="beneficiary.district",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "User Profile",
                "verbose_name_plural": "User Profiles",
            },
        ),
    ]
