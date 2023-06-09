# Generated by Django 3.2.15 on 2023-02-11 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0024_alter_investigationsmolecular_s8_path_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigationslabs',
            name='normal_range_max',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='investigationslabs',
            name='normal_range_min',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
    ]
