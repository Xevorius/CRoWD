from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.email}'s profile"

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img_width, img_height = img.size
            size = min(img.size)
            cropped_img = img.crop(((img_width - size) // 2,
                                 (img_height - size) // 2,
                                 (img_width + size) // 2,
                                 (img_height + size) // 2))
            output_size = (300, 300)
            cropped_img.thumbnail(output_size)
            cropped_img.save(self.image.path)


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, **kwargs):
    if not Profile.objects.filter(user=instance.pk):
        Profile.objects.create(user=instance)


@receiver(pre_delete, sender=get_user_model())
def delete_user_profile(sender, instance, **kwargs):
    profile = Profile.objects.filter(user=instance.pk)
    profile.delete()
