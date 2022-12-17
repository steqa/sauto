from django.urls import path
from . import views

urlpatterns = [
    path('announcements/', views.announcements, name='announcements'),
    path('announcement/<int:pk>/', views.show_announcement, name='show-announcement'),
    path('add-announcement/', views.add_announcement, name='add-announcement'),
]
