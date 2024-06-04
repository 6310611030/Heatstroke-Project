from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import  UserCreationForm, UserinfoForm
from django.contrib import messages
from sensor.models import SensorData
from sensor.views import check_high_risk

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('users:home'))
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'users/login.html', {
                'message': 'You are logged out.'
            })

def home(request):
    high_risk = None
    if request.user.is_authenticated:
        high_risk = check_high_risk(request)
        try:
            latest_data = SensorData.objects.filter(user=request.user).latest('timestamp')
        except SensorData.DoesNotExist:
            latest_data = 0  # Set default value to 0 when no data exists
    else:
        latest_data = None
    context = {'latest_data': latest_data,
               'high_risk': high_risk,}
    return render(request, 'users/home.html', context)

def sign_up(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        userinfo_form = UserinfoForm(request.POST)
        if user_form.is_valid() and userinfo_form.is_valid():
            user = user_form.save()
            userinfo = userinfo_form.save(commit=False)
            userinfo.user = user 
            userinfo.save()
            messages.success(request, 'User created successfully!')
            return redirect('users:login')
    else:
        user_form = UserCreationForm()
        userinfo_form = UserinfoForm()
        if request.user.is_authenticated:
            return redirect('sensor:display_data')
    return render(request, 'users/sign_up.html', {'user_form': user_form, 'userinfo_form': userinfo_form})

@login_required(login_url='/user/login')   
def latest(request):
    high_risk = None
    if request.user.is_authenticated:
        try:
            latest_data = SensorData.objects.filter(user=request.user).latest('timestamp')
        except SensorData.DoesNotExist:
            latest_data = None  # Set default value to 0 when no data exists
        high_risk = check_high_risk(request)
    else:
        latest_data = None
    context = {'latest_data': latest_data,
               'high_risk': high_risk,}
    return render(request, 'users/latest.html', context)


def risk_info(request):

    return render(request, 'users/risk_info.html')
