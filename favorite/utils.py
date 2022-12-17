from sauto.utils import Response
from .models import Favorite


def add_favorite_or_error(request, announcement_pk: int) -> Response:
    favorite, created = Favorite.objects.get_or_create(
        user=request.user, announcement_id=announcement_pk)
    if created:
        response = Response(
            body={'OK': 'OK'},
            type='OK', status=200)
    else:
        response = Response(
            body={'error': 'Это объявление уже находится в избранных.'},
            type='ValidationError', status=400)
    return response


def remove_favorite_or_error(request, announcement_pk: int) -> Response:
    favorite = Favorite.objects.filter(
        user=request.user, announcement_id=announcement_pk).first()
    if favorite:
        favorite.delete()
        response = Response(
            body={'OK': 'OK'},
            type='OK', status=200)
    else:
        response = Response(
            body={'error': 'Этого объявления нет в избранных.'},
            type='ValidationError', status=400)
    return response