from django.utils.datastructures import MultiValueDict
from sauto.utils import Response
from phonenumber_field.phonenumber import PhoneNumber
from seller.models import Seller
from .models import Announcement, AnnouncementImage
from .forms import AnnouncementCreationForm
from seller.utils import is_seller
from sauto.utils import validate_form_data


def validate_images(images: MultiValueDict) -> Response:
    error = {}
    status = 200
    for image in images:
        image_format = images[image].name.split('.')[-1]
        image_size = images[image].size
        if image_size > 1000000:
            error[image] = ['Максимальный размер изображения 1МБ.']
            status = 400
                     
        if (image_format != 'jpg') and (image_format != 'png'):
            error[image] = ['Допустимые форматы изображения JPG или PNG.']
            status = 400
    
    if len(images) < 1:
        error['images'] = ['Добавьте хотя бы одно изображение.']
        status = 400
    elif len(images) > 8:
        error['images'] = ['Вы можете добавить до 8 изображений.']
        status = 400
    
    return Response(body=error, type='ImageValidationError', status=status)


def validate_seller_data(data: dict) -> Response:
    error = {}
    status = 200
    region = data['phone_number_0']
    number = data['phone_number_1']
    telegram_username = data['telegram_username']
    if number != '' and region != None:
        try:
            phone_number = PhoneNumber.from_string(phone_number=number, region=region).as_e164
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
    
    return Response(body=error, type='ValidationError', status=status)


def merge_responses(*args: Response) -> Response:
    merged_body = {}
    merged_status = 200
    merged_type = 'OK'
    for a in args:
        for b in a.body:
            merged_body[b] = a.body[b]
        if a.status == 400 and a.type != 'OK':
            merged_status = 400
            merged_type = 'ValidationError'
    
    return Response(body=merged_body, type=merged_type, status=merged_status)


def get_all_data_from_announcement_creation_page(request) -> dict:
    data = {}
    announcement_data = {}
    announcement_data['category'] = request.POST.get('category')
    announcement_data['condition'] = request.POST.get('condition')
    announcement_data['type_announcement'] = request.POST.get('type_announcement')
    announcement_data['name'] = request.POST.get('name')
    announcement_data['price'] = request.POST.get('price')
    announcement_data['description'] = request.POST.get('description')
    announcement_data['communication_method'] = request.POST.get('communication_method')
    announcement_data['latitude'] = request.POST.get('latitude')
    announcement_data['longitude'] = request.POST.get('longitude')
    seller_data = {}
    seller_data['telegram_username'] = request.POST.get('telegram_username')
    seller_data['phone_number_0'] = request.POST.get('phone_number_0')
    seller_data['phone_number_1'] = request.POST.get('phone_number_1')
    images = request.FILES
    data['announcement_data'] = announcement_data
    data['seller_data'] = seller_data
    data['images'] = images
    return data


def validate_all_data_from_announcement_creation_page(data: dict) -> Response:
    announcement_form_data = AnnouncementCreationForm(data['announcement_data'])
    announcement_data_response = validate_form_data(form_data=announcement_form_data)
    seller_data_response = validate_seller_data(data=data['seller_data'])
    images_response = validate_images(data['images'])
    response = merge_responses(announcement_data_response, seller_data_response, images_response)
    return response


def get_or_create_seller(request, data: dict) -> Seller:
    if not is_seller(request.user):
        communication_method = data['announcement_data']['communication_method']
        user = request.user
        telegram_username = None
        phone_number = None
        if communication_method == '1':
            telegram_username = data['seller_data']['telegram_username']
        elif communication_method == '2':
            phone_number = PhoneNumber.from_string(
                phone_number=data['seller_data']['phone_number_1'],
                region=data['seller_data']['phone_number_0']).as_e164
        
        seller = Seller.objects.create(
            user=user,
            telegram_username=telegram_username,
            phone_number=phone_number
        )
    else:
        seller = Seller.objects.get(user=request.user)
    
    return seller


def create_and_get_announcement(seller: Seller, data: dict) -> Announcement:
    announcement_form_data = AnnouncementCreationForm(data['announcement_data'])
    announcement = announcement_form_data.save(commit=False)
    announcement.seller = seller
    announcement.latitude = data['announcement_data']['latitude']
    announcement.longitude = data['announcement_data']['longitude']
    announcement.save()
    return announcement


def create_announcement_images(announcement: Announcement, data: dict):
    images = data['images']
    for image in images:
        image = images[image]
        AnnouncementImage.objects.create(
            announcement=announcement,
            image=image
        )