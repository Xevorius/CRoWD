from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from authenticators.user_authenticator import UserAuthenticator
from payment.models import Payment
from .models import UserWallet, UserWalletTransaction, User
from .serializers import UserWalletSerializer, UserWalletTransactionSerializer, DepositSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = UserWallet.objects.all()
    serializer_class = DepositSerializer

    @staticmethod
    def get(request) -> Response:
        """
        This function is linked to the auth/user path of this API. It will return the basic information about the
        authenticated user in a http request.

        @param request: Http request containing the JWT token as a cookie.
        @return: Http response containing some basic information about the user.
        """
        user = UserAuthenticator(request)
        queryset = UserWallet.objects.filter(user=user['id'])
        serializer = UserWalletSerializer(queryset.first(), many=False)
        return Response(serializer.data)

    @staticmethod
    def post(request) -> Response:
        """
        This function is linked to the auth/login path of this API. It will take the inputted credentials and varify
        them. If the credentials are correct, this function will return a JWT token that is valid for 1 day.

        @param request: Http containing the credentials of a user
        @return: Http response containing the JWT token as well as a cookie containing
        the same token under variable 'jwt'
        """
        user = UserAuthenticator(request)
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            payment = Payment(user=User.objects.get(pk=user['id']), amount=serializer.data['amount'],
                              email=serializer.data['email'])
            payment.save()
            return render(request, 'make_payment.html', {'payment': payment,
                                                         'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletTransactionsViewSet(viewsets.ModelViewSet):
    queryset = UserWalletTransaction.objects.all()
    serializer_class = UserWalletTransactionSerializer

    def list(self, request) -> Response:
        """
        This function is linked to the auth/user path of this API. It will return the basic information about the
        authenticated user in a http request.

        @param request: Http request containing the JWT token as a cookie.
        @return: Http response containing some basic information about the user.
        """

        try:
            user = UserAuthenticator(request)
            wallet = UserWallet.objects.filter(user=user['id'])
            queryset = UserWalletTransaction.objects.filter(wallet=wallet[0].id)
            serializer = UserWalletTransactionSerializer(queryset, many=True)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)

    def retrieve(self, request, pk=None) -> Response:
        """
        This function is linked to the auth/user path of this API. It will return the basic information about the
        authenticated user in a http request.

        @param request: Http request containing the JWT token as a cookie.
        @return: Http response containing some basic information about the user.
        """
        try:
            user = UserAuthenticator(request)
            wallet = UserWallet.objects.filter(user=user['id'])
            if pk not in [i.id for i in UserWalletTransaction.objects.filter(wallet=wallet[0].id)]:
                return Response("Not your transaction", status=400)
            queryset = self.get_object()
            serializer = UserWalletTransactionSerializer(queryset)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)
