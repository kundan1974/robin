# Generated by Django 3.2.15 on 2023-02-18 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0038_alter_acutetoxicity_tox_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='s4rt',
            name='rtstatus',
            field=models.ForeignKey(db_column='rtstatus', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='rtstatus', to='patient_data.rtstatus'),
        ),
    ]
