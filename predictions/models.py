from django.db import models

# Create your models here.
class ServerActivity(models.Model):
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_io = models.FloatField()
    network_traffic = models.FloatField()
    error_count = models.IntegerField()
    
    
    # Optional: This is for storing the predicted result.
    target = models.IntegerField(choices=[(0, 'Normal'), (1, 'Abnormal')], null=True, blank=True)

    def __str__(self):
        return f"Activity Record (ID: {self.id})"