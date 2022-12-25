from django.urls import reverse
from accounts.models import User
from accounts.forms import UserChangeForm
from sauto.utils import get_form_data, validate_form_data, Response

def change_user_data(request, data):
    field = list(data['formData'].keys())[0] if len(list(data['formData'].keys())) > 0 else None
    form_data = get_form_data(request, UserChangeForm)
    if (request.GET.get('reload')) and (field not in form_data.errors):
        user = User.objects.filter(pk=request.user.pk)
        success = ''
        if field == 'first_name':
            user.update(first_name=form_data.cleaned_data.get('first_name'))
            success = 'Имя изменено.'
        elif field == 'last_name':
            user.update(last_name=form_data.cleaned_data.get('last_name'))
            success = 'Фамилия изменена.'
        elif field == 'email':
            user.update(email=form_data.cleaned_data.get('email'))
            success = 'Адрес электронной почты изменен.'
            
        response = Response(
            body={'success': success, 'url': request.build_absolute_uri(reverse('user-settings'))},
            type='redirect', status=200)
    else:
        response = validate_form_data(form_data=form_data)

    return response