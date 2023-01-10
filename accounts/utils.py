from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from sauto.utils import Response
from .tokens import email_token
from .models import User
from .threads import SendEmailThread


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


def update_user_profile_image(request) -> Response:
    try:
        first_image = list(request.FILES.values())[0]
        user = request.user
        user.profile_image = first_image
        user.save()
        response = Response(
            body={'success': 'Изображение профиля изменено.',
                  'url': request.build_absolute_uri(reverse('user-settings'))},
            type='redirect', status=200)
    except:
        response = Response(
            body={'error': 'Не удалось изменить изображение профиля.'},
            type='BadRequest', status=400)
    
    return response