# Generated by Django 3.2.15 on 2023-04-22 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0054_alter_tnm_p_tx'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouptnm',
            name='stage',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
