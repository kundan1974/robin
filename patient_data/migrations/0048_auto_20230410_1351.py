# Generated by Django 3.2.15 on 2023-04-10 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0047_alter_simulation_finalstatus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='s1parentmain',
            options={'managed': True, 'ordering': ['-last_updated']},
        ),
        migrations.AddField(
            model_name='s5chemoprotocol',
            name='chemo_cycles',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='s5chemoprotocol',
            name='protocol_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='s2diagnosis',
            name='dx_date',
            field=models.DateTimeField(null=True),
        ),
    ]
