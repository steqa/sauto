from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.user_settings, name='user-settings'),
]
