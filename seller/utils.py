from django.utils.datastructures import MultiValueDict
from sauto.utils import Response
from phonenumber_field.phonenumber import PhoneNumber
from accounts.models import User
from .models import Seller


def is_seller(user: User) -> bool:
    return True if Seller.objects.filter(user=user).first() else False


def validate_images(images: MultiValueDict) -> Response:
    error = {}
    if len(images) > 8:
        error['images'] = ['Вы можете загрузить до 8 изображений.']
    
    for image in images:
        image_format = images[image].name.split('.')[-1]
        image_size = images[image].size
        image_name = images[image].name
        if image_size > 1000000:
            error[image_name] = ['Максимальный размер изображения 1МБ.']
                                 
        if (image_format != 'jpg') and (image_format != 'png'):
            error[image_name] = ['Допустимые форматы изображения JPG или PNG.']
    
    return Response(body=error, type='ImageValidationError', status=400)


def validate_seller_data(data: dict) -> Response:
    error = {}
    region = data['formData']['phone_number_0']
    number = data['formData']['phone_number_1']
    try:
        phone_number = PhoneNumber.from_string(phone_number=number, region=region).as_e164
    except:
        if region == '':
            error['phone_number_0'] = ['Выберите регион.']
        
        error['phone_number_1'] = ['Введите корректный номер телефона.']
            
    
    telegram_username = data['formData']['telegram_username']
    if len(telegram_username) > 32:
        error['telegram_username'] = [f'Убедитесь, что это значение содержит не более 32 символов (сейчас {len(telegram_username)}).']
    elif len(telegram_username) < 5:
        error['telegram_username'] = [f'Убедитесь, что это значение содержит не менее 5 символов (сейчас {len(telegram_username)}).']
        
    return Response(body=error, type='ValidationError', status=400)