# Generated by Django 3.1.13 on 2021-11-27 01:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("beneficiary", "0015_auto_20211126_0754"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="lab",
            options={"verbose_name": "Lab", "verbose_name_plural": "Labs"},
        ),
        migrations.AlterModelOptions(
            name="prescription",
            options={
                "verbose_name": "Prescription",
                "verbose_name_plural": "Prescriptions",
            },
        ),
    ]
