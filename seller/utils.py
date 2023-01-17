from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers.phonenumberutil import country_code_for_region
from accounts.models import User
from .models import Seller
from sauto.utils import merge_responses, Response

def validate_seller_data(data: dict) -> Response:
    phone_number_response = validate_phone_number(data)
    telegram_username_response = validate_telegram_username(data)
    response = merge_responses(phone_number_response, telegram_username_response)
    return response


def validate_phone_number(data: dict) -> Response:
    error = {}
    response_status = 200
    response_type = 'OK'
    region = data['phone_number_0'] if 'phone_number_0' in data.keys() else ''
    number = data['phone_number_1'] if 'phone_number_1' in data.keys() else ''
    try:
        phone_number = PhoneNumber.from_string(phone_number=number, region=region).as_e164
        if Seller.objects.filter(phone_number=phone_number).exists():
            error['phone_number_1'] = ['Номер телефона занят.']
            response_status = 400
            response_type = 'ValidationError'
    except:
        if region == '':
            error['phone_number_0'] = ['Выберите регион.']
        error['phone_number_1'] = ['Введите корректный номер телефона.']
        response_status = 400
        response_type = 'ValidationError'
    
    return Response(body=error, type=response_type, status=response_status)


def validate_telegram_username(data: dict) -> Response:
    error = {}
    response_status = 200
    response_type = 'OK'
    telegram_username = data['telegram_username'] if 'telegram_username' in data.keys() else ''
    if len(telegram_username) > 32:
        error['telegram_username'] = [f'Убедитесь, что это значение содержит не более 32 символов (сейчас {len(telegram_username)}).']
        response_status = 400
        response_type = 'ValidationError'
    elif len(telegram_username) < 5:
        error['telegram_username'] = [f'Убедитесь, что это значение содержит не менее 5 символов (сейчас {len(telegram_username)}).']
        response_status = 400
        response_type = 'ValidationError'
    
    if Seller.objects.filter(telegram_username=telegram_username).exists():
        error['telegram_username'] = ['Имя пользователя телеграм занято.']
        response_status = 400
        response_type = 'ValidationError'
    
    return Response(body=error, type=response_type, status=response_status)


def get_or_create_seller(request, telegram_username: None | str, phone_number: None | str) -> Seller:
    if not is_seller(request.user):
        if telegram_username == '':
            telegram_username = None
            
        user = request.user
        seller = Seller.objects.create(
            user=user,
            telegram_username=telegram_username,
            phone_number=phone_number
        )
    else:
        seller = Seller.objects.get(user=request.user)
    
    return seller


def is_seller(user: User) -> bool:
    try:
        return True if Seller.objects.filter(user=user).first() else False
    except:
        return False


def get_telegram_username_and_phone_number_from_data(data):
    telegram_username = data['telegram_username'] if 'telegram_username' in data.keys() else None
    region = data['phone_number_0'] if 'phone_number_0' in data.keys() else None
    number = data['phone_number_1'] if 'phone_number_1' in data.keys() else None
    if region and number:
        country_code = country_code_for_region(region)
        phone_number = '+' + str(country_code) + str(number)
    else:
        phone_number = None
        
    return telegram_username, phone_number