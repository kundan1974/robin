# Generated by Django 3.2.15 on 2023-04-22 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0053_alter_tnm_c_tx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tnm',
            name='p_tx',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
