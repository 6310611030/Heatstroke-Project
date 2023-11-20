from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import SensorData
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

@csrf_exempt
def receive_sensor_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        body_temp = data.get('bodyTemp')

        if 'user' in data:
            username = data['user']
            user, created = User.objects.get_or_create(username=username)
        else:
            user = User.objects.get(username='admin')

        sensor_data = SensorData(temperature=temperature, humidity=humidity, body_temp=body_temp, user=user)
        sensor_data.save()


        response_data = {
            'temperature': temperature,
            'humidity': humidity,
            'body_temp': body_temp,
            'user': user.username,
        }
        return JsonResponse(response_data)
    else:
        return HttpResponse("Invalid request method", status=400)
    
def display_received_data(request):
    sensor_data = SensorData.objects.last()
    data = {
        'temperature': sensor_data.temperature,
        'humidity': sensor_data.humidity,
        'body_temp': sensor_data.body_temp,
    }

    return render(request, 'sensor/receive.html', data)
