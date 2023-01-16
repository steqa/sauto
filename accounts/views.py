from . import constants
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .threads import DeleteUserAfterTimeElapsed
from .tokens import email_token
from .forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .utils import send_email, get_user_by_uidb64, get_user_uidb64
from sauto.utils import validate_form_data, get_form_data, Response
from .models import User
from .decorators import unauthenticated_user


@unauthenticated_user
def registration_user(request):
    form = UserCreationForm
    if request.method == 'POST':
        form_data = get_form_data(request, UserCreationForm)
        if request.GET.get('reload') and form_data.is_valid():
            user = form_data.save()
            send_email(request, user,
                       email_subject='sauto: подтверждение адреса электронной почты',
                       email_template='accounts/registration/verification-email.html')
            DeleteUserAfterTimeElapsed(
                user, constants.LIFETIME_EMAIL_USER_ACTIVATION).start()
            template = render_to_string('accounts/confirm-email.html',
                                        {'user': user}, request),
            response = Response(
                body={'success': 'ConfirmEmail',
                      'template': template,
                      'uidb64': get_user_uidb64(user)},
                type='OK', status=200)
        else:
            response = validate_form_data(form_data=form_data)
        
        return JsonResponse(response._asdict())
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/registration/registration.html', context)


@unauthenticated_user
def activate_user(request, uidb64: str, token: str):
    user = get_user_by_uidb64(uidb64)
    if (user is not None
        and email_token.check_token(user, token, constants.LIFETIME_EMAIL_USER_ACTIVATION)
            and not user.is_email_verified):
        user.is_email_verified = True
        user.save()
        return redirect('login-user')
    else:
        return render(request, 'accounts/registration/user-verification-failed.html', {'user': user})


@unauthenticated_user
def resend_verification_email(request, uidb64: str):
    user = get_user_by_uidb64(uidb64)
    if user is not None and not user.is_email_verified:
        send_email(request, user,
                   email_subject='sauto: подтверждение адреса электронной почты',
                   email_template='accounts/registration/verification-email.html')
        response = Response(
            body={'success': 'Письмо отправленно.'},
            type='OK', status=200)
    else:
        response = Response(
            body={'error': f'Не удалось отправить письмо.'},
            type='EmailSendingError', status=400)
    
    return JsonResponse(response._asdict())
    

@unauthenticated_user
def login_user(request):
    form = AuthenticationForm
    if request.method == 'POST':
        form_data = get_form_data(request, AuthenticationForm)
        if request.GET.get('reload') and form_data.is_valid():
            email = form_data.cleaned_data.get('email')
            password = form_data.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                response = Response(
                    body={'success': f'Добро пожаловать, {user.first_name}.', 'url': request.build_absolute_uri(reverse('announcements'))},
                    type='redirect', status=200)
            else:
                response = Response(
                    body={'error': f'Неверный пароль или адрес электронной почты.'},
                    type='AuthenticationError', status=400)
        else:
            response = validate_form_data(form_data=form_data)

        return JsonResponse(response._asdict())

    context = {
        'form': form
    }
    return render(request, 'accounts/login/login.html', context)


@unauthenticated_user
def reset_password(request):
    form = PasswordResetForm
    if request.method == 'POST':
        form_data = get_form_data(request, PasswordResetForm)
        if request.GET.get('reload') and form_data.is_valid():
            email = form_data.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                send_email(request, user,
                           email_subject='sauto: восстановление пароля',
                           email_template='accounts/reset-password/reset-password-email.html')
                template = render_to_string(
                    'accounts/confirm-email.html', {'user': user}, request),
                response = Response(
                    body={'success': 'ConfirmEmail',
                          'template': template,
                          'uidb64': get_user_uidb64(user)},
                    type='OK', status=200)
            else:
                response = Response(
                    body={'error': f'Пользователь с таким адресом электронной почты не найден.'},
                    type='NotFound', status=400)
        else:
            response = validate_form_data(form_data=form_data)
        
        return JsonResponse(response._asdict())

    context = {
        'form': form,
    }
    return render(request, 'accounts/reset-password/reset-password.html', context)


@unauthenticated_user
def reset_password_confirm(request, uidb64: str, token: str):
    user = get_user_by_uidb64(uidb64)
    if (user is not None and
            email_token.check_token(user, token, constants.LIFETIME_EMAIL_RESET_PASSWORD)):
        form = SetPasswordForm(user)
        if request.method == 'POST':
            form_data = get_form_data(request, SetPasswordForm, user)
            if request.GET.get('reload') and form_data.is_valid():
                form_data.save()
                response = Response(
                    body={'success': f'Вы успешно сменили пароль.', 'url': request.build_absolute_uri(reverse('login-user'))},
                    type='redirect', status=200)
            else:
                response = validate_form_data(form_data=form_data)
            
            return JsonResponse(response._asdict())
        
        context = {
            'form': form,
            'uidb64': uidb64,
            'token': token,
        }
        return render(request, 'accounts/reset-password/reset-password-confirm.html', context)
    else:
        return render(request, 'accounts/reset-password/reset-password-failed.html', {'user': user})


def logout_user(request):
    logout(request)
    return redirect('announcements')