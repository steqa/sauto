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


class AnnouncementSale(models.Model):
    CATEGORIES = (
        (0, 'Прочее'),
        (1, 'Женский гардероб'),
        (2, 'Мужской гардероб'),
        (3, 'Детский гардероб'),
        (4, 'Детские товары'),
        (5, 'Хэндмейд'),
        (6, 'Телефоны и планшеты'),
        (7, 'Фото и видеокамеры'),
        (8, 'Компьютерная техника'),
        (9, 'ТВ, аудио, видео'),
        (10, 'Бытовая техника'),
        (11, 'Для дома и дачи'),
        (12, 'Стройматериалы и инструменты'),
        (13, 'Красота и здоровье'),
        (14, 'Спорт и отдых'),
        (15, 'Хобби и развлечения'),
    )
    
    CONDITION = (
        (0, 'БУ'),
        (1, 'Новое')
    )
    
    TYPE_ANNOUNCEMENT = (
        (0, 'Продаю свое'),
        (1, 'Приобрел на продажу'),
        (2, 'Магазин'),
    )
    
    seller = models.ForeignKey(Seller, verbose_name="продавец", on_delete=models.CASCADE,)
    category = models.IntegerField(verbose_name="категория", choices=CATEGORIES)
    condition = models.IntegerField(verbose_name="состояние", choices=CONDITION)
    type_announcement = models.IntegerField(verbose_name="тип объявления", choices=TYPE_ANNOUNCEMENT)
    name = models.CharField(verbose_name="название", max_length=50)
    price = models.DecimalField(verbose_name="цена", max_digits=13, decimal_places=2)
    description = models.CharField(verbose_name="описание", max_length=3000)
    sold = models.BooleanField(verbose_name="продано", default=False)
    date_created = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="дата изменения", auto_now_add=True)
    
    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'
    
    def __str__(self):
        return self.name if len(self.name) <= 25 else f'{self.name[0:25]}...'


def _get_announcement_sale_image_filepath(self, image_name):
    return f'user_images/{self.announcement_sale.seller.user.pk}/{self.announcement_sale.pk}/{image_name}'


class AnnouncementSaleImage(models.Model):
    announcement_sale = models.ForeignKey(AnnouncementSale, verbose_name="объявление",  on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="изображение", upload_to=_get_announcement_sale_image_filepath)
    
    class Meta:
        verbose_name = 'изображение объявления'
        verbose_name_plural = 'изображения объявлений'
    
    def __str__(self):
        return self.image.name.split('/')[-1]