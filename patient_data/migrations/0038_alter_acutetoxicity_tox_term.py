# Generated by Django 3.2.15 on 2023-02-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0037_auto_20230215_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acutetoxicity',
            name='tox_term',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
