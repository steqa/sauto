import json
from typing import NamedTuple, Literal
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import email_token
from .forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import User
from .threads import SendEmailThread


class Response(NamedTuple):
    body: dict
    type: Literal['OK'] | \
          Literal['redirect'] | \
          Literal['ValidationError'] | \
          Literal['BadRequest'] | \
          Literal['EmailSendingError'] | \
          Literal['AuthenticationError'] | \
          Literal['NotFound']
    status: Literal[200] | Literal[400]


def validate_form_data(form_data:
                       UserCreationForm |
                       AuthenticationForm |
                       PasswordResetForm |
                       SetPasswordForm) -> Response:
    try:
        if form_data.is_valid():
            return Response(body={}, type='OK', status=200)
        else:
            error = {}
            for field in form_data.errors:
                error[field] = [field_errors for field_errors in form_data.errors[field]]
            return Response(body=error, type='ValidationError', status=400)
    except:
        return Response(
            body={'error': 'Некорректные данные.'},
            type='BadRequest', status=400)


def send_email(request, user: User, email_subject: str, email_template: str):
    email_subject = email_subject
    email_body = render_to_string(email_template, {
        'user': user,
        'domain': get_current_site(request),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': email_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER, to=[user.email])

    SendEmailThread(email).start()


def get_user_by_uidb64(uidb64: str) -> User | None:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    return user


def get_user_uidb64(user: User) -> str:
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    return uidb64


def get_form_data(request, Form, *args):
    data = json.loads(request.body)
    form_data = Form(*args, data['form_data'])
    return form_data