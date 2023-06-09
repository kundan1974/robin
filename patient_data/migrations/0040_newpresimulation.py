# Generated by Django 3.2.15 on 2023-02-19 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patient_data', '0039_alter_s4rt_rtstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewPreSimulation',
            fields=[
                ('presimid', models.AutoField(db_column='presimID', primary_key=True, serialize=False)),
                ('day1date', models.DateTimeField(blank=True, null=True)),
                ('day', models.CharField(blank=True, max_length=45, null=True)),
                ('ul_amp', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('ll_amp', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('average_amp', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('ahd', models.IntegerField(blank=True, null=True)),
                ('al', models.BooleanField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=45, null=True)),
                ('last_updated', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('assessedby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='assessedby', to=settings.AUTH_USER_MODEL)),
                ('final_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patient_data.rttech')),
                ('presimparent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patient_data.s1parentmain', to_field='crnumber')),
                ('s3_id', models.ForeignKey(blank=True, db_column='s3_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='patient_data.s3careplan')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patient_data.presimstatus')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'new_presimulation',
            },
        ),
    ]
