from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import SensorData
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models.functions import TruncDay
from django.utils.timezone import localtime
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages


@csrf_exempt
def receive_sensor_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        body_temp = data.get('bodyTemp')
        heart_rate = data.get('bpm')
        risk = data.get('risk')

        if 'user' in data:
            username = data['user']
            user, created = User.objects.get_or_create(username=username)
        else:
            user = User.objects.get(username='test')

        

        sensor_data = SensorData(
            temperature=temperature,
            humidity=humidity,
            body_temp=body_temp,
            heart_rate=heart_rate,
            risk=risk,
            user=user
        )
        sensor_data.save()

        response_data = {
            'temperature': temperature,
            'humidity': humidity,
            'body_temp': body_temp,
            'heart_rate': heart_rate,
            'risk': risk,
            'user': user.username,
            'message': 'Sensor data received successfully.'
        }
        return JsonResponse(response_data)
    else:
        return HttpResponse("Invalid request method", status=400)

def check_high_risk(request):
    if request.user.is_authenticated:
        sensor_data = SensorData.objects.filter(user=request.user)
        recent_high_risk_data = sensor_data.filter(timestamp__gte=timezone.now() - timedelta(seconds=90), risk__gte=5).first()

        if recent_high_risk_data:
            risk_value = recent_high_risk_data.risk
            if 5 <= risk_value <= 6:
                return "High Risk"
            elif 7 <= risk_value <= 8:
                return "Highest Risk"
        else:
            return None
    else:
        return None


@login_required(login_url='/user/login')    
def display_data(request):
    # Retrieve SensorData objects
    sensor_data = SensorData.objects.filter(user=request.user)

    # Retrieve SensorData objects based on selected date range
    start_date_str = request.GET.get('startDate')
    end_date_str = request.GET.get('endDate')

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else datetime(2023, 1, 1)
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else datetime.now()
    end_date += timedelta(days=1)

    sensor_data = sensor_data.filter(timestamp__range=[start_date, end_date])

    # Extract data for plotting
    timestamps = [timezone.localtime(data.timestamp).strftime('%Y-%m-%d %H:%M:%S') for data in sensor_data]
    temperatures = [data.temperature for data in sensor_data]
    humidity_values = [data.humidity for data in sensor_data]
    body_temps = [data.body_temp for data in sensor_data]
    heart_rates = [data.heart_rate for data in sensor_data]
    risks = [data.risk for data in sensor_data]

    # Calculate daily averages
    daily_averages = sensor_data.annotate(
        day=TruncDay('timestamp')
    ).filter(
        timestamp__range=[start_date, end_date]
    ).values('day').annotate(
        avg_temperature=Avg('temperature'),
        avg_humidity=Avg('humidity'),
        avg_body_temp=Avg('body_temp'),
        avg_heart_rate=Avg('heart_rate'), 
        avg_risk=Avg('risk')
    ).order_by('day')

    combined_plot = [{
        'x': timestamps,
        'y': temperatures,
        'mode': 'lines+markers',
        'name': 'Environment Temperature (°C)'
    }, {
        'x': timestamps,
        'y': body_temps,
        'mode': 'lines+markers',
        'name': 'Body Temperature (°C)'
    }]

    all_plot = [{
        'x': timestamps,
        'y': temperatures,
        'mode': 'lines+markers',
        'name': 'Temperature (°C)'
    }, {
        'x': timestamps,
        'y': humidity_values,
        'mode': 'lines+markers',
        'name': 'Humidity (%)'
    }, {
        'x': timestamps,
        'y': body_temps,
        'mode': 'lines+markers',
        'name': 'Body Temperature (°C)'
    }, {
        'x': timestamps,
        'y': heart_rates,
        'mode': 'lines+markers',
        'name': 'Heart Rate (bpm)'
    }, {
        'x': timestamps,
        'y': risks,
        'mode': 'lines+markers',
        'name': 'Risk'
    }]


    high_risk = check_high_risk(request)

    # Pass the data to the template
    context = {
        'timestamps': json.dumps(timestamps),
        'temperatures': json.dumps(temperatures),
        'humidity_values': json.dumps(humidity_values),
        'body_temps': json.dumps(body_temps),
        'heart_rates': json.dumps(heart_rates),
        'risks': json.dumps(risks),
        'combined_plot': json.dumps(combined_plot),
        'high_risk': high_risk,
        'daily_averages': daily_averages,
        'all_plot': json.dumps(all_plot)
    }

    return render(request, 'sensor/display_data.html', context)

