from django.contrib import admin
from django.urls import path, include

from Users.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('users/', include('Users.urls')),
    path('books/', include('Books.urls')),
    path('reading_lists/', include('ReadingLists.urls')),
]

