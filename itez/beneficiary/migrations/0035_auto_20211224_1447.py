# Generated by Django 3.1.13 on 2021-12-24 14:47

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0034_auto_20211224_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalrecord',
            name='service_facility',
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='approver_signature',
            field=imagekit.models.fields.ProcessedImageField(blank=True, help_text='An image containing the signature of the approver.', null=True, upload_to='other'),
        ),
    ]
