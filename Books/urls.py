from django.urls import path

from Books.views import (BooksView, BookDetailView,
                         update_read_status, UpdateBooksStatusView, library_view)

urlpatterns = [
    path('books/', BooksView.as_view(), name='books'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/update_status/', UpdateBooksStatusView.as_view(), name='update_books_status'),
    path('books/update_read_status/<int:book_id>/', update_read_status, name="update_read_status"),
    path('books/library_view', library_view, name='library_view'),
]
