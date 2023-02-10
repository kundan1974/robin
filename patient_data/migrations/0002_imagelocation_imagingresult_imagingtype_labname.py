# Generated by Django 3.2.15 on 2023-02-08 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageLocation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'patient_data_imagelocation',
            },
        ),
        migrations.CreateModel(
            name='ImagingResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('result', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'patient_data_imagingresult',
            },
        ),
        migrations.CreateModel(
            name='ImagingType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'patient_data_imagingtype',
            },
        ),
        migrations.CreateModel(
            name='LabName',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'patient_data_labname',
            },
        ),
    ]
