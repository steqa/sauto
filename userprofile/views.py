import json
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from accounts.models import User
from seller.models import Seller
from seller.forms import SellerCreationForm
from .utils import change_user_data, change_seller_data


@login_required
def user_settings(request):
    seller_form = SellerCreationForm
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
        elif data['action'] == 'change-seller-data':
            response = change_seller_data(request, data)
            return JsonResponse(response._asdict())
    
    context = {
        'user': user,
        'seller': seller,
        'seller_form': seller_form,
    }
    return render(request, 'userprofile/user-settings.html', context)