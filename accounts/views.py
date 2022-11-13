import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import UserCreationForm
from .utils import validate_form_data


def registration(request):
    form = UserCreationForm

    if request.method == 'POST':
        data = json.loads(request.body)
        validation_data = validate_form_data(data, form)
        if data['reload'] and validation_data:
            pass
            validation_data['redirect'] = reverse('registration')
            return JsonResponse(validation_data)
        else:
            return JsonResponse(validation_data)
            
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/registration.html', context)