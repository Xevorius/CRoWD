from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()

    class Meta:
        ordering = ['created']


class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def last_message(self):
        return self.messages.last()

