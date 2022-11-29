from accounts.models import User
from .models import Seller


def is_seller(user: User) -> bool:
    return True if Seller.objects.filter(user=user).first() else False
