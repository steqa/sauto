import json
from django.http.response import JsonResponse
from django.shortcuts import render
from .forms import AnnouncementCreationForm


def add_announcement(request):
    form = AnnouncementCreationForm
    
    context = {
        'form': form,
    }
    return render(request, 'seller/announcement/add_announcement.html', context)