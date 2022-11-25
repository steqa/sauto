from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'date_joined')
    readonly_fields = ('id', 'preview_inside', 'date_joined', 'last_login')
    fieldsets = (
        (None,
            {'fields': (
                readonly_fields[0],
                'email',
                'password'
        )}),
        ('Персональная информация',
            {'fields': (
                'first_name',
                'last_name',
                'profile_image',
                readonly_fields[1],
        )}),
        ('Права доступа',
            {'fields': (
                'is_active',
                'is_staff',
                'is_admin',
                'is_superuser',
                'is_email_verified',
        )}),
        ('Важные даты',
            {'fields': (
                readonly_fields[2:]
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
    
    def preview_inside(self, img):
        print(img.profile_image)
        return mark_safe(f'<img src="{img.profile_image.url}" style="max-height: 200px;">')
    
    preview_inside.short_description = 'просмотр изображения профиля'