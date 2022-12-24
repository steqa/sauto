from django.shortcuts import render
from accounts.models import User
from seller.models import Seller


def user_settings(request):
    user = User.objects.get(pk=request.user.id)
    try:
        seller = Seller.objects.get(user=user)
    except:
        seller = None
        
    context = {
        'user': user,
        'seller': seller,
    }
    return render(request, 'userprofile/user-settings.html', context)