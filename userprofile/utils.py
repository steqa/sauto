from django.urls import reverse
from accounts.models import User
from accounts.forms import UserChangeForm, PasswordChangeForm
from seller.utils import get_or_create_seller, get_telegram_username_and_phone_number_from_data, validate_telegram_username, validate_phone_number
from sauto.utils import get_form_data, validate_form_data, Response

def change_user_data(request, data):
    field = list(data['formData'].keys())[0] if len(list(data['formData'].keys())) > 0 else None
    form_data = get_form_data(request, UserChangeForm)
    if (request.GET.get('reload')) and (field not in form_data.errors):
        user = User.objects.filter(pk=request.user.pk)
        success = ''
        if field == 'first_name':
            user.update(first_name=form_data.cleaned_data.get('first_name'))
            success = 'Имя изменено.'
        elif field == 'last_name':
            user.update(last_name=form_data.cleaned_data.get('last_name'))
            success = 'Фамилия изменена.'
        elif field == 'email':
            user.update(email=form_data.cleaned_data.get('email'))
            success = 'Адрес электронной почты изменен.'
            
        response = Response(
            body={'success': success, 'url': request.build_absolute_uri(reverse('user-settings'))},
            type='redirect', status=200)
    else:
        response = validate_form_data(form_data=form_data)

    return response


def change_seller_data(request, data):
    field = list(data['formData'].keys())[0] if len(list(data['formData'].keys())) > 0 else None
    if field == 'telegram_username':
        response = validate_telegram_username(data=data['formData'])
    elif field in ['phone_number_0', 'phone_number_1']:
        response = validate_phone_number(data=data['formData'])
    else:
        response = Response(
            body={'error': 'Возникла ошибка.'},
            type='BadRequest', status=400)

    telegram_username, phone_number = get_telegram_username_and_phone_number_from_data(data['formData'])
    if (request.GET.get('reload')) and (response.status == 200):
        seller = get_or_create_seller(request, telegram_username, phone_number)
        success = ''
        if field == 'telegram_username':
            seller.telegram_username = telegram_username
            seller.save()
            success = 'Имя пользователя телеграм изменено.'
        elif field in ['phone_number_0', 'phone_number_1']:
            seller.phone_number = phone_number
            seller.save()
            success = 'Номер телефона изменен.'
            
        response = Response(
            body={'success': success, 'url': request.build_absolute_uri(reverse('user-settings'))},
            type='redirect', status=200)
    
    return response


def change_password(request):
    form_data = get_form_data(request, PasswordChangeForm, request.user)
    if request.GET.get('reload') and form_data.is_valid():
        form_data.save()
        response = Response(
            body={'success': f'Вы успешно сменили пароль. ', 'url': request.build_absolute_uri(reverse('login-user'))},
            type='redirect', status=200)
    else:
        response = validate_form_data(form_data)

    return response