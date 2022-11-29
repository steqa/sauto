from sauto import settings
import json
from django.http.response import JsonResponse
from django.shortcuts import render
from .forms import AnnouncementCreationForm, SellerCreationForm
from .utils import is_seller


def add_announcement(request):
    form = AnnouncementCreationForm
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        
        return JsonResponse({'response': 'response'})
    
    context = {
        'form': form,
        'yandex_map_api_key': settings.YANDEX_MAP_API_KEY,
    }
    
    if not is_seller(request.user):
        seller_form = SellerCreationForm
        context['seller_form'] = seller_form
        
    return render(request, 'seller/announcement/add_announcement.html', context)