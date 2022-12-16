from django.contrib import admin
from .models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'announcement')
    search_fields = ('user', 'announcement')
    list_filter = ('user', 'announcement')
    readonly_fields = ('id',)
    fieldsets = (
        (None,
            {'fields': (
                'id',
                'user',
                'announcement',
        )}),
    )