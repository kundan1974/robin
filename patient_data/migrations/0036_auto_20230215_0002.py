# Generated by Django 3.2.15 on 2023-02-15 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0035_alter_prescription_s8_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigationsimaging',
            name='s7_id',
            field=models.ForeignKey(blank=True, db_column='s7_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='patient_data.s7assessment'),
        ),
        migrations.AlterField(
            model_name='investigationsimaging',
            name='s8_id',
            field=models.ForeignKey(blank=True, db_column='s8_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='patient_data.s8fup'),
        ),
    ]
