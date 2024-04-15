from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from payment.models import Payment
from wallet.models import UserWallet, UserWalletTransaction


class UserWalletSerializer(ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ('balance',)


class UserWalletTransactionSerializer(ModelSerializer):
    class Meta:
        model = UserWalletTransaction
        fields = '__all__'


class DepositSerializer(serializers.Serializer):
    model = Payment

    """
    Serializer for password change endpoint.
    """
    amount = serializers.IntegerField(required=True, min_value=0)
    email = serializers.EmailField(required=True)
