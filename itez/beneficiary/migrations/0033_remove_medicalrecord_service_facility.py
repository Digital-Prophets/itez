# Generated by Django 3.1.13 on 2021-12-21 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0032_merge_20211220_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalrecord',
            name='service_facility',
        ),
    ]
