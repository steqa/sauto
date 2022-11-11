from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        field_classes = {}