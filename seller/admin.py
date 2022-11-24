from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Seller, AnnouncementSale, AnnouncementSaleImage


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_username', 'phone_number')
    search_fields = ('user', 'telegram_username', 'phone_number')


@admin.register(AnnouncementSale)
class AnnouncementSaleAdmin(admin.ModelAdmin):
    # add_form = 
    list_display = ('name', 'seller', 'category', 'condition', 'type_announcement', 'price', 'sold')
    search_fields = ('name', 'category', 'condition', 'type_announcement', 'price')
    readonly_fields = ('id', 'date_created', 'date_updated')
    fieldsets = (
        (None,
            {'fields': (
                readonly_fields[0],
                'name',
                'description',
        )}),
        ('Информация',
            {'fields': (
                'price',
                'category',
                'condition',
                'type_announcement',
        )}),
        ('Состояние',
            {'fields': (
                'sold',
        )}),
        ('Важные даты',
            {'fields': (
                'date_created',
                'date_updated',
        )}),
    )


@admin.register(AnnouncementSaleImage)
class AnnouncementSaleImageAdmin(admin.ModelAdmin):
    # add_form = 
    list_display = ('announcement_sale', 'image', 'preview',)
    readonly_fields = ('preview_inside',)
    
    def preview(self, img):
        return mark_safe(f'<img src="{img.image.url}" style="max-height: 25px;">')
    
    def preview_inside(self, img):
        return mark_safe(f'<img src="{img.image.url}" style="max-height: 200px;">')