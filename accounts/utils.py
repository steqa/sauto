from typing import NamedTuple, Literal
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from .forms import UserCreationForm
from .models import User


class Response(NamedTuple):
    body: dict
    type: Literal['OK'] | Literal['ValidationError'] | Literal['BadRequest'] | Literal['EmailSendingError']
    status: Literal[200] | Literal[400]


def validate_form_data(form_data: UserCreationForm) -> Response:
    try:
        if form_data.is_valid():
            return Response(body={}, type='OK', status=200)
        else:
            error = {}
            for field in form_data.errors:
                error[field] = [field_errors for field_errors in form_data.errors[field]]
            return Response(body=error, type='ValidationError', status=400)
    except:
        return Response(body={'error': 'Некорректные данные.'}, type='BadRequest', status=400)


def send_verification_email(user: User, request) -> bool:
    email_subject = 'sauto: подтверждение адреса электронной почты'
    email_body = render_to_string('accounts/registration/verification-email.html', {
        'user': user,
        'domain': get_current_site(request),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })
    
    email = EmailMessage(subject=email_subject, body=email_body,
                 from_email=settings.EMAIL_FROM_USER, to=[user.email])
    if email.send():
        return True
    else:
        return False
    

def get_user_by_uidb64(uidb64: str) -> User | None:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
        
    return user