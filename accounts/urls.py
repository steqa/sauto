from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration_user, name='registration-user'),
    path('login/', views.login_user, name='login-user'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate-user'),
]
