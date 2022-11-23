from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.utils.functional import lazy
from django.utils.html import format_html, format_html_join
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import User


def _password_validators_help_text_html():
    help_texts = password_validation.password_validators_help_texts()
    help_items = format_html_join(
        "", "<li>{}</li>", ((help_text,) for help_text in help_texts)
    )
    return format_html("<ol>{}</ol>", help_items) if help_items else ""

password_validators_help_text_html = lazy(_password_validators_help_text_html, str)


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
        strip=False,
        help_text=password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'autocomplete': 'new-password',
        }))
    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
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
            'autofocus': 'true',
        }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            "autocomplete": "current-password"
        }))


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email address"),
        max_length=260,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        }))


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        help_text=password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Новый пароль',
            "autocomplete": "new-password"
        }))
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение нового пароля',
            "autocomplete": "new-password"
        }))
