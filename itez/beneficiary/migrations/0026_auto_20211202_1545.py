# Generated by Django 3.1.13 on 2021-12-02 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beneficiary", "0025_auto_20211202_1454"),
    ]

    operations = [
        migrations.AlterField(
            model_name="beneficiary",
            name="art_status",
            field=models.CharField(
                blank=True,
                choices=[("Enrolled", "Enrolled"), ("Not Enrolled", "Not Enrolled")],
                max_length=100,
                null=True,
                verbose_name="ART Status",
            ),
        ),
        migrations.AlterField(
            model_name="beneficiary",
            name="hiv_status",
            field=models.CharField(
                blank=True,
                choices=[("Positive", "Positive"), ("Negative", "Negative")],
                max_length=10,
                null=True,
                verbose_name="HIV Status",
            ),
        ),
    ]
