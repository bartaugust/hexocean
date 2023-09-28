from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    BASIC = 1
    PREMIUM = 2
    ENTERPRISE = 3

    TIER_CHOICES = (
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (ENTERPRISE, 'Enterprise'),
    )
    tier = models.PositiveSmallIntegerField(choices=TIER_CHOICES, blank=True, null=True)
