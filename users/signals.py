from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
# from .models import Profile
from django.dispatch import receiver



# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
