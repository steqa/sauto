import json
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .tokens import account_activation_token
from .forms import UserCreationForm
from .models import User
from .utils import validate_form_data, send_verification_email


def registration(request):
    form = UserCreationForm

    if request.method == 'POST':
        data = json.loads(request.body)
        form_data = UserCreationForm(data['formData'])
        validated_data = validate_form_data(form_data=form_data)
        if data['reload'] and validated_data.status == 200:
            user = form_data.save()
            print(type(user))
            send_verification_email(user, request)
            pass
            validated_data.body['action'] = 'confirm_email'

        return JsonResponse(validated_data._asdict())
            
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/registration/registration.html', context)


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return redirect('registration')
    else:
        print('error')
        return redirect('registration')
        