from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from wallet.models import UserWallet
from .models import Payment

User = get_user_model()


def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Verification successful!")
        wallet = UserWallet.objects.get(pk=payment.user.id)
        wallet.update(balance=wallet.balance + payment.amount)

    else:
        messages.error(request, "Verification Failed.")
    return redirect('user_wallet')

