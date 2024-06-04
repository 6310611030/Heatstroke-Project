from django.contrib import admin
from .models import Userinfo

# Register your models here.


class UserinfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'height', 'age')

admin.site.register(Userinfo, UserinfoAdmin)