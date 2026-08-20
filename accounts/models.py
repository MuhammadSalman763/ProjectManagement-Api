from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('qa', 'QA'),
        ('developer', 'Developer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='developer'
    )

    contact_number = models.BigIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username