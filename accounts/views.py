import json
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .tokens import account_activation_token
from .forms import UserCreationForm
from .utils import validate_form_data, send_verification_email, get_user_by_uidb64, Response


def registration_user(request):
    form = UserCreationForm

    if request.method == 'POST':
        data = json.loads(request.body)
        form_data = UserCreationForm(data['formData'])
        validated_data = validate_form_data(form_data=form_data)
        if data['reload'] and validated_data.status == 200:
            user = form_data.save()
            if send_verification_email(user, request):
                template = render_to_string(
                    'accounts/registration/confirm-email.html',{'user': user}, request),
                response = Response(
                    body={'action': 'confirm_email', 'template': template},
                    type='OK', status=200)
            else:
                user.delete()
                response = Response(
                    body={'error': f'Не удалось отправить письмо с подтверждением на почту: {user.email}'},
                    type='EmailSendingError', status=400)
        else:
            response = validated_data

        return JsonResponse(response._asdict())
            
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/registration/registration.html', context)


def activate_user(request, uidb64, token):
    user = get_user_by_uidb64(uidb64)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return redirect('login-user')
    else:
        return render(request, 'accounts/registration/user-activation-failed.html', {'user': user})


def login_user(request):
    context = {}
    return render(request, 'accounts/login/login.html', context)