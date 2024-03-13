from rest_framework.serializers import ModelSerializer

from wallet.models import UserWallet, UserWalletTransaction


class UserWalletSerializer(ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ('balance',)


class UserWalletTransactionSerializer(ModelSerializer):
    class Meta:
        model = UserWalletTransaction
        fields = '__all__'
