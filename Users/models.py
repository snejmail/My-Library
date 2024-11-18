from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[MinLengthValidator(3)],
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions'
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


