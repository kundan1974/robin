# Generated by Django 3.2.15 on 2023-02-19 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0040_newpresimulation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newpresimulation',
            old_name='day1date',
            new_name='date',
        ),
    ]