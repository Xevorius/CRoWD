from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Chat, Message


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser']


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'created', 'updated', 'text']


class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'users', 'messages', 'created', 'updated']
