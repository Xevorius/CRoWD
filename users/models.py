# from PIL.Image import Image
# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
#
# # Create your models here.
# class User(AbstractUser):
#     name = models.CharField(max_length=255)
#     email = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)
#     username = models.CharField(max_length=255, unique=True)
#     # image = models.ImageField(default='default.jpg', upload_to='profile_pics')
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.username
#
#     def save(self, **kwargs):
#         super().save()
#
#         img = Image.open(self.image.path)
#         if img.height > 300 or img.width > 300:
#             img_width, img_height = img.size
#             size = min(img.size)
#             cropped_img = img.crop(((img_width - size) // 2,
#                                  (img_height - size) // 2,
#                                  (img_width + size) // 2,
#                                  (img_height + size) // 2))
#             output_size = (300, 300)
#             cropped_img.thumbnail(output_size)
#             cropped_img.save(self.image.path)
