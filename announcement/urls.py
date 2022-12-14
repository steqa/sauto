from django.urls import path
from . import views

urlpatterns = [
    path('add-announcement/', views.add_announcement, name='add-announcement'),
    path('announcement/<int:pk>/', views.show_announcement, name='show-announcement'),
]
