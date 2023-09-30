from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser
from django.contrib.postgres.fields import ArrayField


class UserTier(models.Model):
    name = models.CharField(max_length=20, unique=True)
    thumbnail_sizes = ArrayField(models.IntegerField(), default=list)
    is_link_present = models.BooleanField(default=False)
    can_generate_link = models.BooleanField(default=False)


#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     # tier = models.ForeignKey(UserTier, on_delete=models.CASCADE, null=True, blank=True)
#
#     username = models.CharField(max_length=25, unique=True)
#     first_name = models.CharField(max_length=25, blank=True)
#     last_name = models.CharField(max_length=25, blank=True)
#     email = models.EmailField(unique=True)
#
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'username'
#     # REQUIRED_FIELDS = ['user_name']
class User(AbstractUser, PermissionsMixin):
    tier = models.ForeignKey(UserTier, on_delete=models.CASCADE, null=True, blank=True)
