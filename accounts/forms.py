from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email address"),
        max_length=260,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
    }))
    first_name = forms.CharField(
        label=_("First name"),
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя',
    }))
    last_name = forms.CharField(
        label=_("Last name"),
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия',
    }))
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'autocomplete': 'new-password',
    }))
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
            'autocomplete': 'new-password',
    }))
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        field_classes = {}


class AuthenticationForm(forms.Form):
    email = forms.EmailField(
        label=_("Email address"),
        max_length=260,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
    }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            "autocomplete": "current-password"
    }))
    