from sauto import settings
import json
from django.http.response import JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from seller.forms import SellerCreationForm
from seller.utils import is_seller, validate_seller_data, get_or_create_seller, get_telegram_username_and_phone_number_from_data
from sauto.utils import validate_form_data, Response
from .forms import AnnouncementCreationForm
from .utils import validate_images, create_and_get_announcement, create_announcement_images, get_all_data_from_announcement_creation_page, validate_all_data_from_announcement_creation_page, get_contact_info, form_announcements_and_images, paginate_announcements, update_announcement_images, update_announcement
from .models import Announcement, Seller, AnnouncementImage


def announcements(request):
    announcements = Announcement.objects.filter(sold=False)
    categories = Announcement.CATEGORIES[1:]
    conditions = Announcement.CONDITION[1:]
    types_announcement = Announcement.TYPE_ANNOUNCEMENT[1:]
    communication_methods = Announcement.COMMUNICATION_METHOD
    if request.method == 'GET':
        if (request.GET.get('filter')
            or request.GET.get('search')
                or request.GET.get('all')):
            response = form_announcements_and_images(request, announcements)
            return JsonResponse(response._asdict())
    
    page_announcements, paginator = paginate_announcements(request, announcements)
    images = AnnouncementImage.objects.filter(
        announcement__in=page_announcements)
    
    context = {
        'announcements': page_announcements,
        'paginator': paginator,
        'images': images,
        'categories': categories,
        'conditions': conditions,
        'types_announcement': types_announcement,
        'communication_methods': communication_methods,
    }
    return render(request, 'announcement/announcements.html', context)


def show_announcement(request, announcement_pk: int):
    announcement = Announcement.objects.get(pk=announcement_pk)
    seller = Seller.objects.get(pk=announcement.seller.pk)
    images = AnnouncementImage.objects.filter(announcement=announcement)
    if request.method == 'GET':
        if request.GET.get('show-contact-info'):
            response = get_contact_info(request, announcement)
            return JsonResponse(response._asdict())
    context = {
        'announcement': announcement,
        'seller': seller,
        'images': images,
    }
    return render(request, 'announcement/show-announcement.html', context)


@login_required
def add_announcement(request):
    form = AnnouncementCreationForm
    if request.method == 'POST':
        if request.POST.get('action') == 'add-announcement':
            data = get_all_data_from_announcement_creation_page(request)
            response = validate_all_data_from_announcement_creation_page(data)
            if response.status == 200:
                telegram_username, phone_number = get_telegram_username_and_phone_number_from_data(data['seller_data'])
                seller = get_or_create_seller(request, telegram_username, phone_number)
                announcement = create_and_get_announcement(seller, data)
                create_announcement_images(announcement, data)
                response = Response(
                    body={'success': 'Объявление добавлено.',
                          'url': request.build_absolute_uri(reverse('announcements'))},
                    type='redirect', status=200)
            return JsonResponse(response._asdict())
        elif request.POST.get('action') == 'validate-image':
            images = request.FILES
            response = validate_images(images)
            return JsonResponse(response._asdict())
        else:
            data = json.loads(request.body)
            if data['action'] == 'validate-announcement-data':
                form_data = AnnouncementCreationForm(data['formData'])
                response = validate_form_data(form_data=form_data)
                return JsonResponse(response._asdict())
            elif data['action'] == 'validate-seller-data':
                response = validate_seller_data(data=data['formData'])
                return JsonResponse(response._asdict())
    
    context = {
        'form': form,
        'yandex_map_api_key': settings.YANDEX_MAP_API_KEY,
    }
    
    if not is_seller(request.user):
        seller_form = SellerCreationForm
        context['seller_form'] = seller_form
        
    return render(request, 'announcement/add-announcement.html', context)


@login_required
def edit_announcement(request, announcement_pk):
    seller = Seller.objects.get(user=request.user)
    announcement = Announcement.objects.get(pk=announcement_pk, seller=seller)
    images = AnnouncementImage.objects.filter(announcement=announcement)
    form = AnnouncementCreationForm(instance=announcement)
    if request.method == 'POST':
        if request.POST.get('action') == 'edit-announcement':
            data = get_all_data_from_announcement_creation_page(request)
            response = validate_all_data_from_announcement_creation_page(data)
            if response.status == 200:
                update_announcement(announcement, data)
                update_announcement_images(announcement, data)
                response = Response(
                    body={'success': 'Объявление изменено.',
                          'url': request.build_absolute_uri(reverse('announcements'))},
                    type='redirect', status=200)
            return JsonResponse(response._asdict())
        elif request.POST.get('action') == 'validate-image':
            images = request.FILES
            response = validate_images(images)
            return JsonResponse(response._asdict())
        else:
            data = json.loads(request.body)
            if data['action'] == 'validate-announcement-data':
                form_data = AnnouncementCreationForm(data['formData'])
                response = validate_form_data(form_data=form_data)
                return JsonResponse(response._asdict())
        
    context = {
        'form': form,
        'announcement': announcement,
        'images': images,
        'yandex_map_api_key': settings.YANDEX_MAP_API_KEY,
    }
    return render(request, 'announcement/edit-announcement.html', context)


@login_required
def delete_announcement(request, announcement_pk):
    seller = Seller.objects.get(user=request.user)
    try:
        announcement = Announcement.objects.get(pk=announcement_pk, seller=seller)
        announcement.delete()
        response = Response(
            body={'success': 'Объявление удалено.'},
            type='OK', status=200)
    except:
        response = Response(
            body={'error': 'Не удалось удалить объявление.'},
            type='BadRequest', status=400)

    return JsonResponse(response._asdict())


@login_required
def change_sold_status_announcement(request, announcement_pk, status):
    seller = Seller.objects.get(user=request.user)
    particle_not = ''
    if status == 'true':
        status = True
        particle_not = ''
    elif status == 'false':
        status = False
        particle_not = 'не '
    else:
        seller = 'Raise exception'
        
    try:
        announcement = Announcement.objects.get(pk=announcement_pk, seller=seller)
        announcement.sold = status
        announcement.save()
        response = Response(
            body={'success': f'Объявление отмечено как {particle_not}проданное.'},
            type='OK', status=200)
    except:
        response = Response(
            body={'error': f'Не удалось отметить объявление как {particle_not}проданное.'},
            type='BadRequest', status=400)

    return JsonResponse(response._asdict())