# Generated by Django 3.2.15 on 2023-04-28 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='expotoken',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]