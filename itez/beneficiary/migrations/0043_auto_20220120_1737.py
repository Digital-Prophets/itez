# Generated by Django 3.1.13 on 2022-01-20 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0042_auto_20220120_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender'), ('Other', 'Other')], default='Other', max_length=50, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender'), ('Other', 'Other')], default='Other', max_length=100, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Intersex', 'Intersex')], max_length=100, verbose_name='Sex'),
        ),
    ]
