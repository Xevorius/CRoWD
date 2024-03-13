from django.contrib import admin

from wallet.models import UserWallet, UserWalletTransaction

admin.site.register(UserWallet)
admin.site.register(UserWalletTransaction)
