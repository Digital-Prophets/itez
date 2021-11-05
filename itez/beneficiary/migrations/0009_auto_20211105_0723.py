# Generated by Django 3.1.13 on 2021-11-05 07:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0008_beneficiary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='beneficiary_code',
            field=models.UUIDField(default=uuid.UUID('5a537c9c-8bc5-4580-841c-f52626a4d7a8'), editable=False),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='other_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Other Name'),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photo/'),
        ),
    ]
