from django.db import models

from Users.models import User


class Book(models.Model):
    title = models.CharField(
        max_length=200,
    )
    author = models.CharField(
        max_length=100,
    )
    genre = models.CharField(
        max_length=100,
    )
    comment = models.TextField(
        blank=True,
        null=True,
    )
    is_read = models.BooleanField(
        default=False,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        default=1,
    )

    def __str__(self):
        return self.title

