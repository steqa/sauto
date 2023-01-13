from django.db import models
from seller.models import Seller


class UserTelegram(models.Model):
    seller = models.ForeignKey(Seller, verbose_name="продавец", on_delete=models.CASCADE)
    telegram_id = models.PositiveBigIntegerField(verbose_name="идентификатор пользователя телеграм", unique=True)
    notifications_enabled = models.BooleanField(verbose_name="статус уведомлений", default=False)
    
    class Meta:
        verbose_name = 'пользователь телеграм'
        verbose_name_plural = 'пользователи телеграм'
    
    def __str__(self):
        return self.telegram_id