from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_admin', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'is_admin', 'is_staff')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()
    