from django.contrib import admin
from .models import ReadingList, ReadingListEntry


class ReadingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'book_count',)
    search_fields = ('name', 'user__username', 'description',)
    list_filter = ('user',)
    ordering = ('name',)

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Number of books'


class ReadingListEntryAdmin(admin.ModelAdmin):
    list_display = ('reading_list', 'book',)
    search_fields = ('reading_list__name', 'book__title',)
    list_filter = ('reading_list',)
    ordering = ('reading_list', 'book',)


admin.site.register(ReadingList, ReadingListAdmin)
admin.site.register(ReadingListEntry, ReadingListEntryAdmin)
