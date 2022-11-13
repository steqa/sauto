from django.shortcuts import render
from .forms import UserCreationForm


def registration(request):
    form = UserCreationForm
    context = {
        'form': form,
    }
    return render(request, 'accounts/registration.html', context)