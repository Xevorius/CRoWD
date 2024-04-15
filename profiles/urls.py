from django.urls import path

from profiles.views import ProfileViewSet

urlpatterns = [
    path('', ProfileViewSet.as_view({'get': 'get', 'put': 'update'}), name='user_profile'),
]