from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, UpdateView

from Books.models import Book
from ReadingLists.models import ReadingList


class BooksView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/books.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('user_sort_by', 'title')
        order = self.request.GET.get('user_order', 'asc')

        if sort_by == 'title':
            queryset = queryset.order_by('title' if order=='asc' else '-title')
        elif sort_by == 'author':
            queryset = queryset.order_by('author' if order == 'asc' else '-author')
        elif sort_by == 'genre':
            queryset = queryset.order_by('genre' if order == 'asc' else '-genre')

        return queryset


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

