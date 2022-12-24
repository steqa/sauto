from django.http.response import JsonResponse
from sauto.utils import Response
from .models import Favorite


def add_favorite(request, announcement_pk: int):
    if request.user.is_authenticated:
        try:
            favorite, created = Favorite.objects.get_or_create(
                user=request.user, announcement_id=announcement_pk)
            if created:
                response = Response(
                    body={'OK': 'OK'},
                    type='OK', status=200)
            else:
                raise Exception
        except:
            response = Response(
                body={'error': 'Произошла ошибка.'},
                type='BadRequest', status=400)
    else:
        response = Response(
            body={'error': 'Для добавления объявления в избранное необходимо войти в систему.'},
            type='AuthenticationError', status=400)
        
    return JsonResponse(response._asdict())


def remove_favorite(request, announcement_pk: int):
    try:
        favorite = Favorite.objects.filter(
            user=request.user, announcement_id=announcement_pk).first()
        if favorite:
            favorite.delete()
            response = Response(
                body={'OK': 'OK'},
                type='OK', status=200)
        else:
            raise Exception
    except:
        response = Response(
            body={'error': 'Произошла ошибка.'},
            type='BadRequest', status=400)
        
    return JsonResponse(response._asdict())