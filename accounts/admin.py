from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import UserCreationForm


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'date_joined')
    readonly_fields = ('id', 'date_joined', 'last_login')
    fieldsets = (
        (None,
            {'fields': (
                readonly_fields[0],
                'email',
                'password'
        )}),
        (_('Personal info'),
            {'fields': (
                'first_name',
                'last_name',
                'profile_image'
        )}),
        (_('Permissions'),
            {'fields': (
                'is_active',
                'is_staff',
                'is_admin',
                'is_superuser',
        )}),
        (_('Important dates'),
            {'fields': (
                readonly_fields[1:]
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    ordering = ()
    filter_horizontal = ()
    list_filter = ()