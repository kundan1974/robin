# Generated by Django 3.2.15 on 2023-02-09 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0005_alter_investigationsimaging_imaging_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investigationsimaging',
            name='imaging_type',
        ),
        migrations.DeleteModel(
            name='ImagingType',
        ),
    ]
