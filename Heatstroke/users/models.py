from django.db import models
from django.contrib.auth.models import User

class Userinfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return f'{ self.user.username } { self.weight } { self.height } { self.age }'