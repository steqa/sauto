from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from accounts.models import User 


class Seller(models.Model):
    user = models.OneToOneField(User, verbose_name="пользователь", on_delete=models.CASCADE)
    telegram_username = models.CharField(verbose_name="имя пользователя телеграм", max_length=32, unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name="номер телефона", unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'продавец'
        verbose_name_plural = 'продавцы'
    
    def __str__(self):
        return self.user.email
