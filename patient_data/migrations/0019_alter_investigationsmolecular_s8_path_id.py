# Generated by Django 3.2.15 on 2023-02-10 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0018_latetoxicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigationsmolecular',
            name='s8_path_id',
            field=models.ForeignKey(db_column='s8_path_id', on_delete=django.db.models.deletion.RESTRICT, to='patient_data.investigationspath'),
        ),
    ]
