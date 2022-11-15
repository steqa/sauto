from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate-user'),
]
