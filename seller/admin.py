from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Seller, Announcement, AnnouncementImage


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_username', 'phone_number')
    search_fields = ('user', 'telegram_username', 'phone_number')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'condition', 'type_announcement', 'price', 'sold')
    search_fields = ('name', 'category', 'condition', 'type_announcement', 'price')
    list_filter = ('category', 'condition', 'type_announcement', 'sold')
    readonly_fields = ('id', 'date_created', 'date_updated')
    fieldsets = (
        (None,
            {'fields': (
                readonly_fields[0],
                'seller',
        )}),
        ('Информация',
            {'fields': (
                'name',
                'description',
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


@admin.register(AnnouncementImage)
class AnnouncementImageAdmin(admin.ModelAdmin):
    list_display = ('announcement_sale', 'image', 'preview',)
    readonly_fields = ('preview_inside',)
    
    def preview(self, img):
        return mark_safe(f'<img src="{img.image.url}" style="max-height: 25px;">')
    
    preview.short_description = 'предпросмотр изображения'
    
    def preview_inside(self, img):
        return mark_safe(f'<img src="{img.image.url}" style="max-height: 200px;">')
    
    preview_inside.short_description = 'просмотр изображения'