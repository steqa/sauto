import json
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from accounts.models import User
from accounts.forms import PasswordChangeForm
from seller.models import Seller
from seller.forms import SellerCreationForm
from announcement.models import Announcement, AnnouncementImage
from announcement.utils import paginate_announcements, form_announcements_and_images
from favorite.models import Favorite
from .utils import change_user_data, change_seller_data, change_password


@login_required
def user_settings(request):
    seller_form = SellerCreationForm
    password_change_form = PasswordChangeForm(request.user)
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
        elif data['action'] == 'change-user-password':
            response = change_password(request)
            return JsonResponse(response._asdict())
    
    context = {
        'seller_form': seller_form,
        'password_change_form': password_change_form,
        'user': user,
        'seller': seller,
    }
    return render(request, 'userprofile/user-settings.html', context)


def user_announcements(request, user_pk):
    user = User.objects.get(id=user_pk)
    seller = Seller.objects.get(user=user)
    announcements = Announcement.objects.filter(seller=seller)
    
    if request.method == 'GET':
        if (request.GET.get('search')
                or request.GET.get('all')
                    or request.GET.get('filter_by_seller_and_sold')):
            response = form_announcements_and_images(request, announcements)
            return JsonResponse(response._asdict())
            
        
    page_announcements, paginator = paginate_announcements(request, announcements)
    images = AnnouncementImage.objects.filter(
        announcement__in=page_announcements)
    context = {
        'user': user,
        'announcements': page_announcements,
        'paginator': paginator,
        'images': images,
    }
    return render(request, 'userprofile/user-announcements.html', context)


@login_required
def user_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    announcements_pk = [favorite.announcement.pk for favorite in favorites]
    announcements = Announcement.objects.filter(pk__in=announcements_pk)
    
    if request.method == 'GET':
        if (request.GET.get('search')
                or request.GET.get('all')):
            response = form_announcements_and_images(request, announcements)
            return JsonResponse(response._asdict())
    
    page_announcements, paginator = paginate_announcements(request, announcements)
    images = AnnouncementImage.objects.filter(
        announcement__in=page_announcements)
    context = {
        'announcements': page_announcements,
        'images': images,
        'paginator': paginator,
    }
    return render(request, 'userprofile/user-favorites.html', context)
    