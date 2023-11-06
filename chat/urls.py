from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoute),
    path('chats/', views.get_chats),
    path('chats/<str:pk>/', views.get_user_chats),
]

