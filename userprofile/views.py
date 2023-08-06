import json
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from accounts.models import User
from accounts.forms import PasswordChangeForm
from accounts.utils import update_user_profile_image
from seller.models import Seller
from seller.forms import SellerCreationForm
from announcement.models import Announcement, AnnouncementImage
from announcement.utils import paginate_announcements, form_announcements_and_images, validate_images
from favorite.models import Favorite
from telegrambot.models import UserTelegram
from .utils import change_user_data, change_seller_data, change_password


@login_required
def user_settings(request):
    seller_form = SellerCreationForm
    password_change_form = PasswordChangeForm(request.user)
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        seller = None
    
    try:
        user_telegram = UserTelegram.objects.get(seller=seller)
    except UserTelegram.DoesNotExist:
        user_telegram = None
    
    if request.method == 'POST':
        if request.POST.get('action') == 'validate-image':
            images = request.FILES
            response = validate_images(images)
            if ((response.status == 200) and (request.GET.get('reload'))):
                response = update_user_profile_image(request)
            
            return JsonResponse(response._asdict())
        else:
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
        'user': request.user,
        'seller': seller,
        'user_telegram': user_telegram,
    }
    return render(request, 'userprofile/user-settings.html', context)


def user_announcements(request, user_pk):
    user = User.objects.get(pk=user_pk)
    try:
        seller = Seller.objects.get(user=user)
    except:
        seller = None
    
    if seller:
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
    else:
        context = {
            'user': user,
            'announcements': None,
            'paginator': None,
            'images': None,
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
    