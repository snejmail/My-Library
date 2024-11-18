from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
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
        return reverse('reading_lists/my_reading_lists')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context


class ReadingListDeleteView(LoginRequiredMixin, DeleteView):
    model = ReadingList
    template_name = 'reading_lists/delete_reading_list.html'
    success_url = reverse_lazy('reading_lists')

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)


@login_required
def choose_reading_list(request):
    # Fetch all reading lists for the current user
    reading_lists = ReadingList.objects.filter(user=request.user)

    if request.method == 'POST':
        selected_list_id = request.POST.get('reading_list')

        if selected_list_id:
            try:
                selected_list = ReadingList.objects.get(id=selected_list_id, user=request.user)
                selected_books = request.session.get('selected_books', [])

                # Debugging: Print or log selected_books and selected_list_id
                print(f"Selected Books: {selected_books}")
                print(f"Selected Reading List ID: {selected_list_id}")

                # Check if there are selected books to add
                if selected_books:
                    for book_id in selected_books:
                        # Get book instance and add it to the reading list
                        book = Book.objects.get(id=book_id)
                        selected_list.books.add(book)

                    # Clear the session after adding books
                    request.session['selected_books'] = []

                return redirect('reading_lists')  # Redirect to the list of reading lists after saving

            except ReadingList.DoesNotExist:
                return render(request, 'reading_lists/choose_reading_list.html', {
                    'reading_lists': reading_lists,
                    'error_message': 'Reading list not found.'
                })
            except Book.DoesNotExist:
                return render(request, 'reading_lists/choose_reading_list.html', {
                    'reading_lists': reading_lists,
                    'error_message': 'One or more books not found.'
                })

    return render(request, 'reading_lists/choose_reading_list.html', {
        'reading_lists': reading_lists
    })


@login_required
def select_reading_list(request):
    reading_lists = ReadingList.objects.filter(user=request.user)

    if request.method == "POST":
        select_reading_list_id = request.POST.get('reading_list')
        selected_books = request.session.get('selected_books', [])

        if select_reading_list_id and selected_books:
            reading_list = get_object_or_404(
                ReadingList,
                id=select_reading_list_id,
                user=request.user
            )

            for book_id in selected_books:
                book = get_object_or_404(Book, id=book_id)
                reading_list.books.add(book)

            request.session['selected_books'] = []

            return redirect('books')

    return render(
        request,
        'reading_lists/choose_reading_list.html',
        {'reading_lists': reading_lists},
    )


