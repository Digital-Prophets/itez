# Generated by Django 3.1.13 on 2021-11-03 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Province')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Province',
                'verbose_name_plural': 'Provinces',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='WorkDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.IntegerField(verbose_name='Monthly Salary')),
                ('company', models.CharField(max_length=200, verbose_name='Company Name')),
                ('insured', models.CharField(choices=[('Yes', 1), ('No', 2)], default='Yes', max_length=100, verbose_name='Is your company insured?')),
                ('work_address', models.CharField(max_length=500, verbose_name='Work Address')),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='District')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='beneficiary.province')),
            ],
        ),
    ]
