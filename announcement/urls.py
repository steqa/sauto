from django.urls import path
from . import views

urlpatterns = [
    path('', views.announcements, name='announcements'),
    path('announcement/<int:announcement_pk>/', views.show_announcement, name='show-announcement'),
    path('add-announcement/', views.add_announcement, name='add-announcement'),
    path('edit-announcement/<int:announcement_pk>/', views.edit_announcement, name='edit-announcement'),
    path('delete-announcement/<int:announcement_pk>/', views.delete_announcement, name='delete-announcement'),
    path('change-sold-status-announcement/<int:announcement_pk>/<str:status>/', views.change_sold_status_announcement, name='change-sold-status-announcement'),
]
