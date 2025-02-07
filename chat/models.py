from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.text}"

    class Meta:
        ordering = ['created']


class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def last_message(self):
        return self.messages.last()

