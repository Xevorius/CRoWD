from django.urls import path

from payment.views import verify_payment
from wallet.views import WalletViewSet, WalletTransactionsViewSet

urlpatterns = [
    path('transactions/', WalletTransactionsViewSet.as_view({'get': 'list'}), name='user_wallet'),
    path('transactions/<int:pk>/', WalletTransactionsViewSet.as_view({'get': 'retrieve'})),
    path('', WalletViewSet.as_view({'get': 'get', 'post': 'post'}), name='user_wallet'),
    path('<str:ref>/', verify_payment, name="verify-payment"),
]
