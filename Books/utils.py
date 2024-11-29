from Books.models import Book


def get_sorted_books(request):
    books = Book.objects.all()

    sort_by = request.GET.get('user_sort_by', 'title')
    order = request.GET.get('user_order', 'asc')

    if sort_by == 'title':
        books = books.order_by('title' if order == 'asc' else '-title')
    elif sort_by == 'author':
        books = books.order_by('author' if order == 'asc' else '-author')
    elif sort_by == 'genre':
        books = books.order_by('genre' if order == 'asc' else '-genre')

    return books