import json
from django.http.response import JsonResponse
from django.shortcuts import render
from .forms import UserCreationForm
from .utils import validate_form_data


def registration(request):
    form = UserCreationForm

    if request.method == 'POST':
        data = json.loads(request.body)
        form_data = UserCreationForm(data['formData'])
        validated_data = validate_form_data(form_data=form_data)
        if data['reload'] and validated_data.status == 200:
            pass
            validated_data.body['action'] = 'confirm_email'

        return JsonResponse(validated_data._asdict())
            
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/registration.html', context)