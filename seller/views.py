from sauto import settings
import json
from django.http.response import JsonResponse
from django.shortcuts import render
from .forms import AnnouncementCreationForm


def add_announcement(request):
    form = AnnouncementCreationForm
    if request.method == 'POST':
        if request.POST.get('action') == 'send-image':
            print('files')
            print(request.FILES)
        else:
            data = json.loads(request.body)
            print('data')
            print(data)

        return JsonResponse({'response': 'response'})
        
    
    context = {
        'form': form,
        'yandex_map_api_key': settings.YANDEX_MAP_API_KEY,
    }
    return render(request, 'seller/announcement/add_announcement.html', context)