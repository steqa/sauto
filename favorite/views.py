from django.shortcuts import render
from django.http.response import JsonResponse
from sauto.utils import Response
from .models import Favorite


def add_favorite(request, user_pk: int, announcement_pk: int):
    try:
        favorite, created = Favorite.objects.get_or_create(
            user_id=user_pk, announcement_id=announcement_pk)
        if not created:
            response = Response(
                body={'error': 'Это объявление уже находится в избранных.'},
                type='ValidationError', status=400)
        else:
            response = Response(
                body={'OK': 'OK'},
                type='OK', status=200)
    except:
        response = Response(
            body={'error': 'BadRequest'},
            type='BadRequest', status=400)
        
    return JsonResponse(response._asdict())


def remove_favorite(request, user_pk: int, announcement_pk: int):
    try:
        favorite = Favorite.objects.filter(
            user_id=user_pk, announcement_id=announcement_pk).first()
        if favorite:
            favorite.delete()
            response = Response(
                body={'OK': 'OK'},
                type='OK', status=200)
        else:
            response = Response(
                body={'error': 'Этого объявления нет в избранных.'},
                type='ValidationError', status=400)
    except:
        response = Response(
            body={'error': 'BadRequest'},
            type='BadRequest', status=400)
        
    return JsonResponse(response._asdict())