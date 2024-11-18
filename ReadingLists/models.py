from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models

from Books.models import Book
from Users.models import User


class ReadingList(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(3)],
    )
    description = models.TextField(
        blank=True,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='reading_lists',
    )
    books = models.ManyToManyField(
        to=Book,
        blank=True,
        related_name='reading_lists',
    )

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class ReadingListEntry(models.Model):
    reading_list = models.ForeignKey(
        to=ReadingList,
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.book.title} in {self.reading_list.name}"

