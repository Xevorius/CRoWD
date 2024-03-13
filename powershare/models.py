from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PowerShareStation(models.Model):
    lat = models.FloatField(max_length=100)
    lon = models.FloatField(max_length=100)
    uuid = models.CharField(max_length=100)
    deviceId = models.CharField(max_length=100, primary_key=True)
    model = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


class PowerShareOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickupStation = models.ForeignKey(PowerShareStation, on_delete=models.CASCADE, related_name='pick_up_station')
    returnStation = models.ForeignKey(PowerShareStation, on_delete=models.CASCADE, related_name='return_station', blank=True, null=True)
    pickupTime = models.DateTimeField()
    returnTime = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
