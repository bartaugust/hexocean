from django.db import models
# from django.contrib.auth.models import Group
# from django.contrib.auth.models import AbstractUser

from django.contrib.postgres.fields import ArrayField


class UserTier(models.Model):
    name = models.CharField(max_length=20, unique=True)
    thumbnail_sizes = ArrayField(models.IntegerField(), default=list)
    is_link_present = models.BooleanField(default=False)
    can_generate_link = models.BooleanField(default=False)


# class User(AbstractUser):
#     tier = models.ForeignKey(UserTier, on_delete=models.CASCADE, null=True, blank=True)
    # BASIC = 1
    # PREMIUM = 2
    # ENTERPRISE = 3
    #
    # TIER_CHOICES = (
    #     (BASIC, 'Basic'),
    #     (PREMIUM, 'Premium'),
    #     (ENTERPRISE, 'Enterprise'),
    # )
    # tier = models.PositiveSmallIntegerField(choices=TIER_CHOICES, blank=True, null=True)

# basic_user_group = Group.objects.create(name='Basic')
# premium_user_group = Group.objects.create(name='Premium')
# enterprise_user_group = Group.objects.create(name='Enterprise')
