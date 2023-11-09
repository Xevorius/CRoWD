from django.urls import path
from .views import ChatViewSet, MessageViewSet, UserViewSet

urlpatterns = [
    path('chats/', ChatViewSet.as_view({'get': 'list', 'post': 'create'}), name='chats'),
    path('chats/<int:pk>/', ChatViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='chat_detail'),
    path('messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='messages'),
    path('messages/<int:pk>/', MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='message_detail'),
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='users'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),name='user_detail'),
]

