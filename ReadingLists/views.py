from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from Books.models import Book
from ReadingLists.forms import ReadingListForm
from ReadingLists.models import ReadingList


class ReadingListView(LoginRequiredMixin, ListView):
    model = ReadingList
    template_name = 'reading_lists/my_reading_lists.html'
    context_object_name = 'reading_lists'

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)


class ReadingListCreateView(LoginRequiredMixin, CreateView):
    model = ReadingList
    form_class = ReadingListForm
    template_name = 'reading_lists/create_reading_list.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('reading_lists')


class ReadingListUpdateView(LoginRequiredMixin, UpdateView):
    model = ReadingList
    form_class = ReadingListForm
    template_name = 'reading_lists/edit_reading_list.html'

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('reading_lists')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()

        self.request.session['current_reading_list_id'] = self.object.id

        return context


class ReadingListDeleteView(LoginRequiredMixin, DeleteView):
    model = ReadingList
    template_name = 'reading_lists/delete_reading_list.html'
    success_url = reverse_lazy('reading_lists')

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)


@login_required
def select_reading_list(request):
    reading_lists = ReadingList.objects.filter(user=request.user)

    if request.method == "POST":
        if 'reading_list' in request.POST:
            select_reading_list_id = request.POST.get('reading_list')

            if not select_reading_list_id:
                return render(request, 'reading_lists/choose_reading_list.html', {
                    'reading_lists': reading_lists,
                    'error_message': "Please first select a reading list from 'My Reading Lists' tab."
                })

            request.session['current_reading_list_id'] = select_reading_list_id

            return redirect('books')

        elif 'books' in request.POST:
            selected_books = request.POST.getlist('books')

            if not selected_books:
                return render(request, 'books/books.html', {
                    'books': Book.objects.all(),
                    'error_message': "No books selected."
                })

            current_reading_list_id = request.session.get('current_reading_list_id')
            if not current_reading_list_id:
                return render(request, 'books/books.html', {
                    'books': Book.objects.all(),
                    'error_message': "Please first select a reading list."
                })

            reading_list = get_object_or_404(ReadingList, id=current_reading_list_id, user=request.user)

            already_in_list_message = []

            for book_id in selected_books:
                book = get_object_or_404(Book, id=book_id)

                if reading_list.books.filter(id=book.id).exists():
                    already_in_list_message.append(f"'{book.title}' is already in your reading list.")
                else:
                    reading_list.books.add(book)

            request.session['selected_books'] = []

            if already_in_list_message:
                error_message = " ".join(already_in_list_message)
                return render(request, 'books/books.html', {
                    'books': Book.objects.all(),
                    'error_message': error_message,
                })

            return redirect('edit_reading_list', pk=current_reading_list_id)

    return render(request, 'reading_lists/choose_reading_list.html', {
        'reading_lists': reading_lists,
    })

