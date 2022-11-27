import json
from django.http.response import JsonResponse
from django.shortcuts import render
from .forms import AnnouncementCreationForm


def add_announcement(request):
    form = AnnouncementCreationForm
    if request.method == 'POST':
        if request.FILES:
            print('files')
            print(request.FILES)
        else:
            data = json.loads(request.body)
            print('data')
            print(data)

        return JsonResponse({'response': 'response'})
        
    
    context = {
        'form': form,
    }
    return render(request, 'seller/announcement/add_announcement.html', context)