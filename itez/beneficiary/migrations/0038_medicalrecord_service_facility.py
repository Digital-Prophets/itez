# Generated by Django 3.1.13 on 2021-12-30 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0037_merge_20211230_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalrecord',
            name='service_facility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='beneficiary.facility'),
        ),
    ]
