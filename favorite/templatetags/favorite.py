from django import template
from announcement.models import Announcement
from accounts.models import User
from favorite.models import Favorite

register = template.Library()

@register.filter(name='is_favorite')
def is_favorite(announcement: Announcement, user: User):
    try:
        return True if Favorite.objects.filter(announcement=announcement, user=user).first() else False
    except:
        return False