from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PowerShareStation(models.Model):
    location = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


class PowerShareOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickupStation = models.ForeignKey(PowerShareStation, on_delete=models.CASCADE, related_name='pick_up_station')
    returnStation = models.ForeignKey(PowerShareStation, on_delete=models.CASCADE, related_name='return_station')
    pickupTime = models.DateTimeField()
    returnTime = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
