# Generated by Django 3.1.13 on 2021-11-26 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beneficiary", "0014_auto_20211125_1425"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="service_type",
            field=models.CharField(
                blank=True,
                choices=[
                    (1, "HTS (HIV Testing Services)"),
                    (2, "LAB"),
                    (3, "PHARMACY"),
                ],
                max_length=255,
                null=True,
                verbose_name="Service Type",
            ),
        ),
    ]
