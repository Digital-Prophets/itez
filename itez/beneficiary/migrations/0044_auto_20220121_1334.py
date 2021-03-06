# Generated by Django 3.1.13 on 2022-01-21 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0043_auto_20220120_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_type',
            field=models.CharField(blank=True, choices=[('HTS', 'HTS (HIV Testing Services)'), ('LAB', 'LAB'), ('PHARMACY', 'PHARMACY'), ('OPD', 'OPD'), ('VL', 'VL')], max_length=255, null=True, verbose_name='Service Type'),
        ),
        migrations.AlterField(
            model_name='service',
            name='title',
            field=models.CharField(blank=True, choices=[('HTS', 'HTS (HIV Testing Services)'), ('LAB', 'Lab Review'), ('PHARMACY', 'Drug Pickup'), ('OPD', 'OPD Services'), ('VL', 'VL Checkup')], max_length=255, null=True, verbose_name='Service Title'),
        ),
    ]
