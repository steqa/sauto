import pytz
from datetime import datetime, timedelta
from sauto import settings
from django.utils.datastructures import MultiValueDict
from django.template.loader import render_to_string
from django.core.paginator import Paginator, Page
from django.db.models.query import QuerySet
from sauto.utils import validate_form_data, merge_responses, Response
from seller.models import Seller
from seller.utils import validate_seller_data, is_seller
from .models import Announcement, AnnouncementImage
from .forms import AnnouncementCreationForm


def validate_images(images: MultiValueDict) -> Response:
    error = {}
    status = 200
    for image in images:
        image_format = images[image].name.split('.')[-1]
        image_size = images[image].size
        if image_size > 1000000:
            error[image] = ['Максимальный размер изображения 1МБ.']
            status = 400
                     
        if (image_format != 'jpg') and (image_format != 'jpeg'):
            error[image] = ['Допустимые форматы изображения JPG или JPEG.']
            status = 400
    
    if len(images) < 1:
        error['images'] = ['Добавьте хотя бы одно изображение.']
        status = 400
    elif len(images) > 8:
        error['images'] = ['Вы можете добавить до 8 изображений.']
        status = 400
    
    return Response(body=error, type='ImageValidationError', status=status)


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
    if not is_seller:
        seller_data_response = validate_seller_data(data['seller_data'])
    else:
        seller_data_response = Response(body={}, type='OK', status=200)
        
    images_response = validate_images(data['images'])
    response = merge_responses(announcement_data_response, seller_data_response, images_response)
    return response


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


def update_announcement(announcement: Announcement, data: dict):
    announcement.category = data['announcement_data']['category']
    announcement.condition = data['announcement_data']['condition']
    announcement.type_announcement = data['announcement_data']['type_announcement']
    announcement.name = data['announcement_data']['name']
    announcement.price = data['announcement_data']['price']
    announcement.description = data['announcement_data']['description']
    announcement.communication_method = data['announcement_data']['communication_method']
    announcement.latitude = data['announcement_data']['latitude']
    announcement.longitude = data['announcement_data']['longitude']
    announcement.save()


def update_announcement_images(announcement: Announcement, data: dict):
    images = data['images']
    images_names_list = [file.name for file in images.values()]
    current_images = AnnouncementImage.objects.filter(announcement=announcement)
    current_images_names_list = [str(file) for file in current_images]
    
    for image in current_images:
        if str(image) not in images_names_list:
            image.delete()

    for image in images.values():
        if image.name not in current_images_names_list:
            AnnouncementImage.objects.create(
                announcement=announcement,
                image=image
            )


def get_contact_info(request, announcement: Announcement) -> Response:
    if request.user.is_authenticated:
        contact_info = None
        contact_type = None
        if announcement.communication_method == 0:
            contact_info = announcement.seller.user.email
            contact_type = 'email'
        elif announcement.communication_method == 1:
            contact_info = announcement.seller.telegram_username
            contact_type = 'telegram_username'
        elif announcement.communication_method == 2:
            contact_info = announcement.seller.phone_number
            contact_type = 'phone_number'
        response = Response(
            body={'contact_type': contact_type, 'contact_info': str(contact_info)},
            type='OK', status=200)
    else:
        response = Response(
            body={'error': 'Для получения контактной информации необходимо войти в систему.'},
            type='AuthenticationError', status=400)
    return response


def form_announcements_and_images(request) -> Response:
    try:
        filtered_announcements = Announcement.objects.all()
        
        if request.GET.get('filter'):
            filtered_announcements = filter_announcements(request, filtered_announcements)
        if request.GET.get('search'):
            filtered_announcements = search_announcements(request, filtered_announcements)
        if request.GET.get('filter_by_seller_and_sold'):
            filtered_announcements = filter_announcements_by_seller_and_sold(request, filtered_announcements)
        
        page_announcements, paginator = paginate_announcements(request, filtered_announcements)
        
        filtered_images = AnnouncementImage.objects.filter(
            announcement__in=page_announcements)
        
        filtered_context = {
            'announcements': page_announcements,
            'paginator': paginator,
            'images': filtered_images,
        }

        template = render_to_string(
            'announcement/announcement-cards.html',
            filtered_context, request)

        response = Response(
            body={'template': template},
            type='OK', status=200)
    except:
        response = Response(
            body={'error': 'Возникла ошибка.'},
            type='BadRequest', status=400)
    
    return response


def filter_announcements(request, filtered_announcements: QuerySet) -> QuerySet:
    price_from = request.GET.get('price-from')
    if price_from is not None:
        filtered_announcements = filtered_announcements.filter(
            price__gte=price_from)
    
    price_to = request.GET.get('price-to')
    if price_to is not None:
        filtered_announcements = filtered_announcements.filter(
            price__lte=price_to)
    
    category = request.GET.get('category')
    if category is not None:
        filtered_announcements = filtered_announcements.filter(
            category__in=category.split(','))
    
    condition = request.GET.get('condition')
    if condition is not None:
        filtered_announcements = filtered_announcements.filter(
            condition__in=condition.split(','))
    
    type_announcement = request.GET.get('type-announcement')
    if type_announcement is not None:
        filtered_announcements = filtered_announcements.filter(
            type_announcement__in=type_announcement.split(','))
    
    communication_method = request.GET.get('communication-method')
    if communication_method is not None:
        filtered_announcements = filtered_announcements.filter(
            communication_method__in=communication_method.split(','))
    
    placement_period = request.GET.get('placement-period')
    if placement_period is not None:
        tz = pytz.timezone(settings.TIME_ZONE)
        datetime_now = datetime.now(tz)
        filter_datetime = None
        
        if placement_period in ['24h', '7d']:
            if placement_period == '24h':
                filter_datetime = datetime_now - timedelta(days=1)
            elif placement_period == '7d':
                filter_datetime = datetime_now - timedelta(days=7)
            filtered_announcements = filtered_announcements.filter(
                date_created__gte=filter_datetime)
    
    return filtered_announcements


def search_announcements(request, filtered_announcements: QuerySet) -> QuerySet:
    q = request.GET.get('search')
    filtered_announcements = filtered_announcements.filter(name__iregex=q)
    return filtered_announcements


def filter_announcements_by_seller_and_sold(request, filtered_announcements: QuerySet) -> QuerySet:
    sold = request.GET.get('sold')
    user_pk = request.GET.get('user_pk')
    seller = Seller.objects.get(user_id=user_pk)
    filtered_announcements = filtered_announcements.filter(seller=seller)
    if sold == 'true':
        filtered_announcements = filtered_announcements.filter(sold=True)
    elif sold == 'false':
        filtered_announcements = filtered_announcements.filter(sold=False)
    return filtered_announcements


def paginate_announcements(request, announcements: QuerySet) -> tuple[Page, Paginator]:
    paginator = Paginator(announcements, 32)
    page = request.GET.get('page')
    page_announcements = paginator.get_page(page)
    return page_announcements, paginator