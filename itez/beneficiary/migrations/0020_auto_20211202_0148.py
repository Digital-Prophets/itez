# Generated by Django 3.1.13 on 2021-12-02 01:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0019_auto_20211201_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalrecord',
            name='service_provider',
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('single', 'Single'), ('married', 'Married'), ('seperated', 'Seperated'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], max_length=100, null=True, verbose_name='Marital Status'),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='parent_details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='beneficiary.beneficiaryparent'),
        ),
    ]