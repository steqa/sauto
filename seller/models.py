from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from accounts.models import User 


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_username = models.CharField(_("telegram username"), max_length=32, unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(_("phone number"), unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.user.email