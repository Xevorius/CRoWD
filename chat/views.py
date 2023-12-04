import jwt
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.response import Response

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

User = get_user_model()


def authCheck(request):
    print(request.data)
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    return payload


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def list(self, request):
        user = authCheck(request)
        queryset = Chat.objects.filter(users=user['id'])
        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = authCheck(request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        user = authCheck(request)
        chat = self.get_object()
        serializer = self.serializer_class(chat)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = authCheck(request)
        chat = self.get_object()
        serializer = self.serializer_class(chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        user = authCheck(request)
        chat = self.get_object()
        chat.delete()
        return Response(status=204)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request):
        user = authCheck(request)
        serializer = self.serializer_class(data=request.data, user=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        user = authCheck(request)
        message = self.get_object()
        serializer = self.serializer_class(message)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = authCheck(request)
        message = self.get_object()
        serializer = self.serializer_class(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        user = authCheck(request)
        message = self.get_object()
        message.delete()
        return Response(status=204)

    def list(self, request, chat_pk=None):
        user = authCheck(request)
        queryset = Message.objects.filter(chat__pk=chat_pk)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, chat_pk=None):
        user = authCheck(request)
        chat = Chat.objects.get(pk=chat_pk)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()  # Save the message to get a message instance
            chat.messages.add(message)  # Add the message to the chat
            chat.save()  # Save the chat
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
