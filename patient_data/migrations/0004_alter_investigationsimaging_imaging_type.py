# Generated by Django 3.2.15 on 2023-02-08 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0003_auto_20230208_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigationsimaging',
            name='imaging_type',
            field=models.ForeignKey(db_column='imaging_type', null=True, on_delete=django.db.models.deletion.CASCADE, to='patient_data.imagingtype', to_field='type'),
        ),
    ]
