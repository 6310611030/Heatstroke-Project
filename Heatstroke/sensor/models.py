from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SensorData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    body_temp = models.FloatField()
    heart_rate = models.IntegerField() 
    risk = models.IntegerField() 
    #timestamp = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.temperature}°C {self.humidity}% {self.body_temp}°C {self.heart_rate}bpm {self.risk} {self.timestamp}"
    
