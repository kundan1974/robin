# Generated by Django 3.2.15 on 2023-02-09 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0009_alter_investigationsimaging_imaging_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
