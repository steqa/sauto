from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:announcement_pk>/', views.add_favorite, name='add-favorite'),
    path('remove/<int:announcement_pk>/', views.remove_favorite, name='remove-favorite'),
]
