# Generated by Django 3.2.15 on 2023-03-26 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0045_auto_20230322_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='finalstatus',
            field=models.CharField(blank=True, db_column='finalstatus', max_length=100, null=True),
        ),
    ]