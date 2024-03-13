from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_init, pre_save, post_save, pre_delete
from django.dispatch import receiver

User = get_user_model()


class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(max_length=100, default=0)

    def __str__(self):
        return f"{self.user.username}'s wallet"


class UserWalletTransaction(models.Model):
    wallet = models.ForeignKey(UserWallet, on_delete=models.CASCADE)
    deposit = models.FloatField(max_length=100)
    balanceBefore = models.FloatField(max_length=100)
    balanceAfter = models.FloatField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=get_user_model())
def create_user_wallet(sender, instance, **kwargs):
    if not UserWallet.objects.filter(user=instance.pk):
        UserWallet.objects.create(user=instance)


@receiver(pre_delete, sender=get_user_model())
def delete_user_wallet(sender, instance, **kwargs):
    wallet = UserWallet.objects.filter(user=instance.pk)
    wallet.delete()
