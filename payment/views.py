from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from requests import Response
from rest_framework.exceptions import AuthenticationFailed

from authenticators.user_authenticator import UserAuthenticator
from wallet.models import UserWallet
from . import forms
from .models import Payment

User = get_user_model()


def initiate_payment(request: HttpRequest) -> HttpResponse:
    user = UserAuthenticator(request)
    if request.method == "POST":
        payment_form = forms.PaymentForm(request.POST)
        payment_form.instance.user = User.objects.get(pk=user['id'])
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'make_payment.html', {'payment': payment,
                                                         'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = forms.PaymentForm()
    return render(request, 'initiate_payment.html', {'payment_form': payment_form})


def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Verification successful!")
        wallet = UserWallet.objects.get(pk=payment.user.id)
        wallet.update(balance=wallet.balance + payment.amount)

    else:
        messages.error(request, "Verification Failed.")
    return redirect('initiate-payment')

