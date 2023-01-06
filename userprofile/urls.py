from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.user_settings, name='user-settings'),
    path('announcements/<int:user_pk>/', views.user_announcements, name='user-announcements'),
    path('favorites/', views.user_favorites, name='user-favorites'),
]
