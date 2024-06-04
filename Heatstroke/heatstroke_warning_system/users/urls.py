from django.urls import path

from . import views
app_name = 'users'  

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('latest/', views.latest, name='latest'),
    path('risk_info/', views.risk_info, name='risk_info'),
]