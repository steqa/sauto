import json
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .tokens import account_activation_token
from .forms import UserCreationForm, AuthenticationForm
from .utils import validate_form_data, send_verification_email, get_user_by_uidb64, Response
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .threads import DeleteUserByTimerThread
from . import constants


def registration_user(request):
    form = UserCreationForm

    if request.method == 'POST':
        data = json.loads(request.body)
        form_data = UserCreationForm(data['formData'])
        validated_data = validate_form_data(form_data=form_data)
        if data['reload'] and validated_data.status == 200:
            user = form_data.save()
            send_verification_email(user, request)
            DeleteUserByTimerThread(user, constants.LIFETIME_OF_THE_EMAIL_FOR_USER_ACTIVATION).start()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            template = render_to_string(
                'accounts/registration/confirm-email.html',{'user': user}, request),
            response = Response(
                body={'action': 'ConfirmEmail', 'template': template, 'uidb64': uidb64},
                type='OK', status=200)
        else:
            response = validated_data

        return JsonResponse(response._asdict())
            
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/registration/registration.html', context)


def activate_user(request, uidb64, token):
    user = get_user_by_uidb64(uidb64)
    if (user is not None and
        account_activation_token.check_token(user, token, constants.LIFETIME_OF_THE_EMAIL_FOR_USER_ACTIVATION) and
        not user.is_email_verified):
        user.is_email_verified = True
        user.save()
        return redirect('login-user')
    else:
        return render(request, 'accounts/registration/user-activation-failed.html', {'user': user})


def resend_activation_email(request):
    data = json.loads(request.body)
    user = get_user_by_uidb64(data['uidb64'])
    if user is not None and not user.is_email_verified:
        send_verification_email(user, request)
        response = Response(
            body={'action': 'SuccessAlert', 'message': 'Письмо отправленно.'},
            type='OK', status=200)
    else:
        response = Response(
            body={'error': f'Не удалось отправить письмо.'},
            type='EmailSendingError', status=400)
        
    return JsonResponse(response._asdict())
    

def login_user(request):
    form = AuthenticationForm
    
    if request.method == 'POST':
        data = json.loads(request.body)
        form_data = AuthenticationForm(data['formData'])
        validated_data = validate_form_data(form_data=form_data)
        if data['reload'] and validated_data.status == 200:
            email = form_data.cleaned_data.get('email')
            password = form_data.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                response = Response(
                    body={'url': request.build_absolute_uri(reverse('home'))},
                    type='redirect', status=200)
            else:
                response = Response(
                    body={'error': f'Неверный пароль или адрес электронной почты'},
                    type='AuthenticationError', status=400)
        else:
            response = validated_data

        return JsonResponse(response._asdict())
    
    context = {
        'form': form
    }
    return render(request, 'accounts/login/login.html', context)