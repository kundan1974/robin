# Generated by Django 3.2.15 on 2023-01-14 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelTrainingStatus',
            fields=[
                ('training_id', models.AutoField(primary_key=True, serialize=False)),
                ('model_id', models.BigIntegerField()),
                ('user_id', models.IntegerField()),
                ('epoch', models.BigIntegerField()),
                ('lr', models.FloatField(default=0.01)),
                ('test_size', models.FloatField(default=0.2)),
                ('batch_size', models.IntegerField()),
                ('csv_file_name', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=25)),
                ('requested_date', models.DateTimeField(auto_now=True)),
                ('training_started_at', models.DateTimeField(blank=True, null=True)),
                ('training_ended_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
