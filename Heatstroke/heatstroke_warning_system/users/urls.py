from django.urls import path

from . import views
app_name = 'users'  

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_user', views.create_user, name='create_user'),
]