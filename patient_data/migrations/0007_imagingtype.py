# Generated by Django 3.2.15 on 2023-02-09 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0006_auto_20230209_0245'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=250)),
                ('type', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'patient_data_imagingtype',
            },
        ),
    ]
