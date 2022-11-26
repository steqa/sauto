from django.urls import path
from . import views

urlpatterns = [
    path('add-announcement/', views.add_announcement, name='add-announcement'),
]
