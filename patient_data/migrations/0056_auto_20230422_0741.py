# Generated by Django 3.2.15 on 2023-04-22 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_data', '0055_grouptnm_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='tnm',
            name='c_t1a1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='c_t1a2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='c_t1b1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='c_t1b2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='c_t1b3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='c_t2a1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='c_t2a2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='c_t3c1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='c_t3c2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='p_t1a1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='p_t1a2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='p_t1b1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='p_t1b2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='p_t1b3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='p_t2a1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='p_t2a2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='p_t3c1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tnm',
            name='p_t3c2',
            field=models.TextField(blank=True, null=True),
        ),
    ]