# Generated by Django 3.2.15 on 2023-02-12 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0028_auto_20230211_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='s5chemoprotocol',
            name='protocol_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
