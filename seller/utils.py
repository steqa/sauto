from phonenumber_field.phonenumber import PhoneNumber
from accounts.models import User
from .models import Seller
from sauto.utils import Response


def validate_seller_data(data: dict) -> Response:
    error = {}
    status = 200
    region = data['phone_number_0'] if 'phone_number_0' in data.keys() else ''
    number = data['phone_number_1'] if 'phone_number_1' in data.keys() else ''
    telegram_username = data['telegram_username'] if 'telegram_username' in data.keys() else ''
    if number != '' and region != '':
        try:
            phone_number = PhoneNumber.from_string(phone_number=number, region=region).as_e164
            if Seller.objects.filter(phone_number=phone_number).exists():
                error['phone_number_1'] = ['Номер телефона занят.']
                status = 400
        except:
            if region == '':
                error['phone_number_0'] = ['Выберите регион.']
            error['phone_number_1'] = ['Введите корректный номер телефона.']
            status = 400
    
    if telegram_username != '':
        if len(telegram_username) > 32:
            error['telegram_username'] = [f'Убедитесь, что это значение содержит не более 32 символов (сейчас {len(telegram_username)}).']
            status = 400
        elif len(telegram_username) < 5:
            error['telegram_username'] = [f'Убедитесь, что это значение содержит не менее 5 символов (сейчас {len(telegram_username)}).']
            status = 400
        
        if Seller.objects.filter(telegram_username=telegram_username).exists():
            error['telegram_username'] = ['Имя пользователя телеграм занято.']
            status = 400
    
    return Response(body=error, type='ValidationError', status=status)


def get_or_create_seller(request, telegram_username: None | str, phone_number: None | str) -> Seller:
    if not is_seller(request.user):
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
        phone_number = PhoneNumber.from_string(
            phone_number=number,
            region=region)
        phone_number = str(phone_number)
    else:
        phone_number = None
        
    return telegram_username, phone_number