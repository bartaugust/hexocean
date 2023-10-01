from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser
from django.contrib.postgres.fields import ArrayField


class UserTier(models.Model):
    name = models.CharField(max_length=20, unique=True)
    thumbnail_sizes = ArrayField(models.IntegerField(), default=list)
    is_link_present = models.BooleanField(default=False)
    can_generate_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(AbstractUser, PermissionsMixin):
    tier = models.ForeignKey(UserTier, on_delete=models.CASCADE, null=True, blank=True)


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=None, related_name='images')

    def __str__(self):
        return f"{self.image}"
