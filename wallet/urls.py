from django.urls import path, include

from wallet.views import WalletViewSet, WalletTransactionsViewSet, DepositToWallet

urlpatterns = [
    path('', WalletViewSet.as_view({'get': 'get'}), name='user_wallet'),
    path('transactions/', WalletTransactionsViewSet.as_view({'get': 'list'}), name='user_wallet'),
    path('transactions/<int:pk>/',
         WalletTransactionsViewSet.as_view({'get': 'retrieve'})),
    path('deposit/', include('payment.urls')),

]