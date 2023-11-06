from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
