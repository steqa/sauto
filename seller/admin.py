from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_username', 'phone_number')
    search_fields = ('user', 'telegram_username', 'phone_number')
