from sauto import settings
import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from seller.forms import SellerCreationForm
from sauto.utils import validate_form_data
from .forms import AnnouncementCreationForm
from .utils import is_seller, validate_images, validate_seller_data, get_or_create_seller, create_and_get_announcement, create_announcement_images, get_all_data_from_announcement_creation_page, validate_all_data_from_announcement_creation_page, get_contact_info, form_announcements
from .models import Announcement, Seller, AnnouncementImage


def announcements(request):
    announcements = Announcement.objects.all()
    images = AnnouncementImage.objects.all()
    categories = Announcement.CATEGORIES[1:]
    conditions = Announcement.CONDITION[1:]
    types_announcement = Announcement.TYPE_ANNOUNCEMENT[1:]
    communication_methods = Announcement.COMMUNICATION_METHOD
    if request.method == 'GET':
        if (request.GET.get('filter')
            or request.GET.get('q')
                or request.GET.get('all')):
            response = form_announcements(request)
            return JsonResponse(response._asdict())
    
    context = {
        'announcements': announcements,
        'images': images,
        'categories': categories,
        'conditions': conditions,
        'types_announcement': types_announcement,
        'communication_methods': communication_methods,
    }
    return render(request, 'announcement/announcements.html', context)


def show_announcement(request, pk: int):
    announcement = Announcement.objects.get(pk=pk)
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
                seller = get_or_create_seller(request, data)
                announcement = create_and_get_announcement(seller, data)
                create_announcement_images(announcement, data)
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