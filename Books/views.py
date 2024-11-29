from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, UpdateView

from Books.models import Book
from Books.utils import get_sorted_books
from ReadingLists.models import ReadingList


class BooksView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/books.html'
    context_object_name = 'books'

    def get_queryset(self):
        return get_sorted_books(self.request)


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
    is_read = request.POST.get('is_read') == 'true'

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


def library_view(request):
    books = get_sorted_books(request)
    return render(request, 'books/library_view.html',
                  {'books': books}
                  )
