import json
from django.http.response import JsonResponse
from django.shortcuts import render
from accounts.models import User
from seller.models import Seller
from .utils import change_user_data


def user_settings(request):
    user = User.objects.get(pk=request.user.id)
    try:
        seller = Seller.objects.get(user=user)
    except:
        seller = None
    
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['action'] == 'change-user-data':
            response = change_user_data(request, data)
            return JsonResponse(response._asdict())
    
    context = {
        'user': user,
        'seller': seller,
    }
    return render(request, 'userprofile/user-settings.html', context)