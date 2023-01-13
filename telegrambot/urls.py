from django.urls import path
from . import views

urlpatterns = [
    path('enable-telegram-notifications/',
         views.enable_telegram_notifications,
         name='enable-telegram-notifications'),
    path('disable-telegram-notifications/',
         views.disable_telegram_notifications,
         name='disable-telegram-notifications'),
]