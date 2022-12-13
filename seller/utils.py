from accounts.models import User
from .models import Seller


def is_seller(user: User) -> bool:
    try:
        return True if Seller.objects.filter(user=user).first() else False
    except:
        return False
