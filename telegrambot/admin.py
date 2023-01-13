from django.contrib import admin
from .models import UserTelegram


@admin.register(UserTelegram)
class UserTelegramAdmin(admin.ModelAdmin):
    list_display = ('seller', 'telegram_id', 'notifications_enabled')
    search_fields = ('seller', 'telegram_id', 'notifications_enabled')
