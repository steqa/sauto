from sauto import settings
import requests


def get_users_list() -> dict:
    request = requests.get(f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates')
    users_list = {}    
    for i in request.json()['result']:
        username = i['message']['chat']['username']
        chat_id = i['message']['chat']['id']
        if not username in users_list:
            users_list[username] = chat_id
    
    return users_list