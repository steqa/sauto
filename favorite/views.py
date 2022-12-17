from django.http.response import JsonResponse
from .utils import add_favorite_or_error, remove_favorite_or_error
from sauto.utils import Response


def add_favorite(request, announcement_pk: int):
    if request.user.is_authenticated:
        try:
            response = add_favorite_or_error(request, announcement_pk)
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
        response = remove_favorite_or_error(request, announcement_pk)
    except:
        response = Response(
            body={'error': 'Произошла ошибка.'},
            type='BadRequest', status=400)
        
    return JsonResponse(response._asdict())