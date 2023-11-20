from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import  UserCreationForm, UserinfoForm
from django.contrib import messages

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

@login_required
def home(request):
    return render(request, 'users/home.html')

def create_user(request):
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
            return redirect('users:home')
    return render(request, 'users/create_user.html', {'user_form': user_form, 'userinfo_form': userinfo_form})