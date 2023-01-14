import os
import requests
from pathlib import Path
from typing import Literal
from django.urls import reverse
from sauto import settings
from favorite.models import Favorite
from .models import UserTelegram


def get_users_list() -> dict:
    request = requests.get(f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates')
    users_list = {}    
    for i in request.json()['result']:
        username = i['message']['chat']['username']
        chat_id = i['message']['chat']['id']
        if not username in users_list:
            users_list[username] = chat_id
    
    return users_list


def send_favorite_notification(request, favorite: Favorite, action: Literal['add', 'remove']):
    try:
        user_telegram = UserTelegram.objects.get(
            seller=favorite.announcement.seller, notifications_enabled=True)
    except UserTelegram.DoesNotExist:
        user_telegram = None
    
    if user_telegram and action in ['add', 'remove']:
        chat_id = user_telegram.telegram_id
        template = form_favorite_notification_text(request, favorite, action)
        
        request = f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={template}&parse_mode=HTML'
        requests.get(request)


def form_favorite_notification_text(request, favorite: Favorite, action: Literal['add', 'remove']) -> str:
    if action == 'add':
        template = 'telegrambot/add-favorite-notification.html'
    elif action == 'remove':
        template = 'telegrambot/remove-favorite-notification.html'
        
    template_path = Path(
        os.path.dirname(os.path.abspath(__file__)) + f'/templates/{template}'
        ).resolve()
    
    with open(template_path, encoding='utf8') as file:
        text = file.read()
        
    text = text.replace('$user_name', f'{favorite.user.first_name} {favorite.user.last_name}')
    text = text.replace('$user_profile_url', request.build_absolute_uri(reverse('user-announcements', kwargs={'user_pk': favorite.user.pk})))
    text = text.replace('$announcement_name', favorite.announcement.name)
    text = text.replace('$announcement_url', request.build_absolute_uri(reverse('show-announcement', kwargs={'announcement_pk': favorite.announcement.pk})))
    text = text.replace('$user_settings_url', request.build_absolute_uri(reverse('user-settings')))
    return text