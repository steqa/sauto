from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('', include('announcement.urls')),
    path('favorite/', include('favorite.urls')),
    path('profile/', include('userprofile.urls')),
    path('telegrambot/', include('telegrambot.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
