from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView, UserQrView, activate, ChangePasswordView, \
    ResetPasswordView, NewPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', UserView.as_view()),
    path('qr/', UserQrView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('wallet/', include('wallet.urls')),
    path('profile/', include('profiles.urls')),
    path('activate/<uid64>/<token>', activate, name='activate'),
    path('password/change', ChangePasswordView.as_view(), name='password_change'),
    path('password/reset', ResetPasswordView.as_view(), name='password_reset'),
    path('password/reset/<uid64>/<token>', NewPasswordView.as_view(), name='pw_confirm'),
]
