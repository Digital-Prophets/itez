# Generated by Django 3.1.13 on 2021-11-03 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0005_auto_20211103_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workdetail',
            name='work_address',
            field=models.TextField(blank=True, null=True, verbose_name='Work Address'),
        ),
    ]
