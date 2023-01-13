from django.http.response import JsonResponse
from django.urls import reverse
from sauto.utils import Response
from seller.models import Seller
from .models import UserTelegram
from .utils import get_users_list


def enable_telegram_notifications(request):
    user = request.user
    
    try:
        seller = Seller.objects.get(user=user)
    except Seller.DoesNotExist:
        response = Response(
            body={'error': 'Для включения уведомлений телеграм необходимо разместить хотя бы 1 объявление.'},
            type='NotFound', status=400)
        return JsonResponse(response._asdict())
    
    users_list = get_users_list()
    try:
        user_telegram_id = users_list[seller.telegram_username]
    except KeyError:
        response = Response(
            body={'error': 'Не удалось найти ваш телеграм профиль. Возможно вы неверно указали имя пользователя телеграм или не активировали бота.'},
            type='NotFound', status=400)
        return JsonResponse(response._asdict())
        
    user_telegram, created = UserTelegram.objects.get_or_create(
        seller=seller,
        telegram_id = user_telegram_id,
    )
    
    if user_telegram.notifications_enabled:
        response = Response(
            body={'error': 'Вы уже включили телеграм уведомления.'},
            type='BadRequest', status=400)
        return JsonResponse(response._asdict())
    else:
        user_telegram.notifications_enabled = True
        user_telegram.save()
    
    response = Response(
        body={'success': 'Теперь вы будете получать уведомления в телеграм.',
              'url': request.build_absolute_uri(reverse('user-settings'))},
        type='redirect', status=200)
    return JsonResponse(response._asdict())


def disable_telegram_notifications(request):
    user = request.user
    try:
        seller = Seller.objects.get(user=user)
        user_telegram = UserTelegram.objects.get(seller=seller)
        user_telegram.notifications_enabled = False
        user_telegram.save()
        response = Response(
            body={'success': 'Теперь вы не будете получать уведомления в телеграм.'},
            type='OK', status=200)
        return JsonResponse(response._asdict())
    except:
        response = Response(
            body={'error': 'Что-то пошло не так.'},
            type='BadRequest', status=400)
        return JsonResponse(response._asdict())