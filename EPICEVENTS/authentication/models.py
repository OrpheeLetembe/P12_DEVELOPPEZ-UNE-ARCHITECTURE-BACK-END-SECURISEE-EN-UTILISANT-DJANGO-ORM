from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    MANAGER ='MANAGER'
    SALE = 'SALE'
    SUPPORT = 'SUPPORT'

    TEAM_CHOICES = (
        (MANAGER, 'Manager'),
        (SALE, 'Sale'),
        (SUPPORT, 'Support')

    )

    mobile = models.CharField(max_length=100)
    team = models.CharField(max_length=100, choices=TEAM_CHOICES)
