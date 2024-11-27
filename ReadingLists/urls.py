from django.urls import path

from .views import ReadingListView, ReadingListCreateView, ReadingListUpdateView, ReadingListDeleteView, \
    select_reading_list

urlpatterns = [
    path('', ReadingListView.as_view(), name='reading_lists'),
    path('create/', ReadingListCreateView.as_view(), name='create_reading_list'),
    path('<int:pk>/edit/', ReadingListUpdateView.as_view(), name='edit_reading_list'),
    path('<int:pk>/delete/', ReadingListDeleteView.as_view(), name='delete_reading_list'),
    path('select_reading_list/', select_reading_list, name='select_reading_list'),
]
