from tokenize import group

from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):

    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné'),
    )

    profile_photo = models.ImageField(verbose_name="Photo de profil", null=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name="Rôle")


    def save(self, *args, **kwargs):
        super.save(*args, **kwargs)
        if self.role == self.CREATOR:
            group = Group.objects.get(name='cretors')
            group.user_set.add(self)
        elif self.role == self.SUBSCRIBER:
            group = Group.objects.get(name='subscribers')
            group.user_set.add(self)
