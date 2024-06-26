from django import forms
from django.contrib.auth.models import User
from .models import Userinfo

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class UserinfoForm(forms.ModelForm):
    class Meta:
        model = Userinfo
        fields = ['weight', 'height', 'age']