# Generated by Django 3.2.15 on 2023-02-27 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0043_alter_simulation_presimid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='s4rt',
            name='simid',
            field=models.ForeignKey(db_column='simid', null=True, on_delete=django.db.models.deletion.RESTRICT, to='patient_data.simulation'),
        ),
    ]
