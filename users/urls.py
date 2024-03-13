from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView, UserQrView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('', UserView.as_view()),
    path('qr/', UserQrView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('wallet/', include('wallet.urls')),
    path('profile/', include('profiles.urls')),
]
