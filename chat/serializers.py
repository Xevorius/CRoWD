from rest_framework.serializers import ModelSerializer
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'created', 'updated', 'text']


class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'users', 'messages', 'created', 'updated']
