from django.urls import path
from . import views

app_name = 'sensor'  
urlpatterns = [
    path('receive/', views.receive_sensor_data, name='receive'),
    path('display_data/', views.display_received_data, name='display_data'),
]