# Generated by Django 3.2.15 on 2023-04-21 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0049_tnm'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupTNM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=100)),
                ('staging_type', models.CharField(max_length=100)),
                ('t', models.CharField(max_length=50)),
                ('n', models.CharField(max_length=50)),
                ('m', models.CharField(max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('her2neu', models.CharField(blank=True, max_length=50, null=True)),
                ('er', models.CharField(blank=True, max_length=50, null=True)),
                ('pr', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'tnm_group',
            },
        ),
    ]