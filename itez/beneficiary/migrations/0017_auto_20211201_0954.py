# Generated by Django 3.1.13 on 2021-12-01 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0016_auto_20211127_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='facility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='beneficiary.facility'),
        ),
        migrations.AlterField(
            model_name='service',
            name='client_type',
            field=models.CharField(blank=True, choices=[('OPD', 'OPD (Outpatient Departments )'), ('ART', 'ART (Antiretroviral Therapy)')], max_length=255, null=True, verbose_name='Client Type'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_type',
            field=models.CharField(blank=True, choices=[('HTS', 'HTS (HIV Testing Services)'), ('LAB', 'LAB'), ('PHARMACY', 'PHARMACY')], max_length=255, null=True, verbose_name='Service Type'),
        ),
    ]
