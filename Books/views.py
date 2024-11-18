import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, UpdateView

from Books.models import Book
from ReadingLists.models import ReadingListEntry, ReadingList


class BooksView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/books.html'
    context_object_name = 'books'


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'


class UpdateBooksStatusView(LoginRequiredMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        book_ids = request.POST.getlist('books')
        Book.objects.update(is_read=False)
        Book.objects.filter(id__in=book_ids).update(is_read=True)
        return redirect('books')


@require_POST
def update_read_status(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    is_read = request.POST.get('is_read') == 'true'  # Properly parse the 'true'/'false' value

    book.is_read = is_read
    book.save()

    if is_read:
        reading_list, created = ReadingList.objects.get_or_create(
            name="Read books",
            user=request.user
        )
        reading_list.books.add(book)
    else:
        reading_list = ReadingList.objects.filter(
            name="Read books",
            user=request.user
        ).first()

        if reading_list:
            reading_list.books.remove(book)

    return JsonResponse({'success': True})


@login_required
def select_books(request):
    if request.method == 'POST':
        selected_books = request.POST.getlist('books')
        request.session['selected_books'] = selected_books
        return redirect('choose_reading_list')
