from django.core.management import BaseCommand
from django.db import models

from Books.models import Book


class Command(BaseCommand):
    help = "Find and remove duplicate books from the database"

    def handle(self, *args, **kwargs):
        duplicates = (
            Book.objects
            .values('title', 'author')
            .annotate(count=models.Count('id'))
            .filter(count__gt=1)
        )

        for duplicate in duplicates:
            title = duplicate['title']
            author = duplicate['author']
            books = Book.objects.filter(title=title, author=author)
            books_to_keep = books.first()
            books.exclude(id=books_to_keep.id).delete()
            self.stdout.write(self.style.SUCCESS(f'Removed duplicates for {title} by {author}'))


