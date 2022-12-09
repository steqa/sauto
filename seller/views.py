from sauto import settings
import json
from django.http.response import JsonResponse
from django.shortcuts import render
from .forms import AnnouncementCreationForm, SellerCreationForm
from .utils import is_seller, validate_images, validate_seller_data, get_all_data_from_announcement_creation_page, validate_all_data_from_announcement_creation_page
from sauto.utils import validate_form_data


def add_announcement(request):
    form = AnnouncementCreationForm
    if request.method == 'POST':
        if request.POST.get('action') == 'add-announcement':
            data = get_all_data_from_announcement_creation_page(request)
            response = validate_all_data_from_announcement_creation_page(data)
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
        
        return JsonResponse({'response': 'response'})
    
    context = {
        'form': form,
        'yandex_map_api_key': settings.YANDEX_MAP_API_KEY,
    }
    
    if not is_seller(request.user):
        seller_form = SellerCreationForm
        context['seller_form'] = seller_form
        
    return render(request, 'seller/announcement/add_announcement.html', context)