# Generated by Django 3.1.13 on 2021-12-02 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0021_auto_20211202_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiary',
            name='facility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='beneficiary.facility'),
        ),
    ]
