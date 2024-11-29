from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'groups')
    ordering = ('username',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)