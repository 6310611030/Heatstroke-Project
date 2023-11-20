from django.contrib import admin
from .models import SensorData
# Register your models here.

class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'temperature', 'humidity', 'body_temp', 'timestamp')

admin.site.register(SensorData, SensorDataAdmin)