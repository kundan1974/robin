from django.db import models

# Create your models here.


class ModelTrainingStatus(models.Model):
    training_id = models.AutoField(primary_key=True)
    model_id = models.BigIntegerField()
    user_id = models.IntegerField()
    epoch = models.BigIntegerField()
    lr = models.FloatField(default=0.01)
    test_size = models.FloatField(default=0.2)
    batch_size = models.IntegerField()
    csv_file_name = models.CharField(max_length=100)
    status = models.CharField(max_length=25)
    requested_date = models.DateTimeField(auto_now=True)
    training_started_at = models.DateTimeField(blank=True, null=True)
    training_ended_at = models.DateTimeField(blank=True, null=True)
