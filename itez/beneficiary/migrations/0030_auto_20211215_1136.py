# Generated by Django 3.1.13 on 2021-12-15 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0029_auto_20211213_1236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beneficiary',
            options={'ordering': ['-created'], 'verbose_name': 'Beneficiary', 'verbose_name_plural': 'Beneficiaries'},
        ),
        migrations.AlterModelOptions(
            name='medicalrecord',
            options={'ordering': ['-created'], 'verbose_name': 'Medical Record', 'verbose_name_plural': 'Medical Records'},
        ),
    ]
