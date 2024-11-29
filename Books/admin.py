from django.contrib import admin

from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'is_read', 'user',)
    search_fields = ('title', 'author', 'genre')
    list_filter = ('author', 'genre', 'is_read', 'user')
    ordering = ('-is_read', 'title')
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, "Selected books marked as read.")


admin.site.register(Book, BookAdmin)
