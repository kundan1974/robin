# Generated by Django 3.2.15 on 2023-02-10 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0016_auto_20230210_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='symptoms',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
