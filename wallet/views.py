from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from authenticators.user_authenticator import UserAuthenticator
from payment import forms
from .models import UserWallet, UserWalletTransaction
from .serializers import UserWalletSerializer, UserWalletTransactionSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = UserWallet.objects.all()
    serializer_class = UserWalletSerializer

    def get(self, request) -> Response:
        """
        This function is linked to the auth/user path of this API. It will return the basic information about the
        authenticated user in a http request.

        @param request: Http request containing the JWT token as a cookie.
        @return: Http response containing some basic information about the user.
        """
        try:
            user = UserAuthenticator(request)
            queryset = UserWallet.objects.filter(user=user['id'])
            serializer = UserWalletSerializer(queryset.first(), many=False)
        except AuthenticationFailed:
            return Response("User authentication failed", status=400)
        return Response(serializer.data)


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


def DepositToWallet(request):
    if request.method == "POST":
        payment_form = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'make_payment.html', {'payment': payment,
                                                         'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = forms.PaymentForm()
    return render(request, 'initiate_payment.html', {'payment_form': payment_form})

