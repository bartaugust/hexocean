from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.contrib.postgres.fields import ArrayField
import uuid
import datetime


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

    def generate_expiring_link(self, time_to_expire):
        link = ExpiringLink(image=self, time_to_expire=time_to_expire)
        link.save()
        return link

    def __str__(self):
        return f"{self.image}"


class ExpiringLink(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    link = models.CharField(max_length=255, default='', editable=False)
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name='expiry_links')
    creation_time = models.DateTimeField(auto_now_add=True)
    time_to_expire = models.IntegerField()

    def expiry_time(self):
        return self.creation_time + datetime.timedelta(seconds=self.time_to_expire)

    def is_expired(self):
        return datetime.datetime.now() > self.expiry_time()
