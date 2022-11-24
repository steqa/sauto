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
    
    seller = models.ForeignKey(Seller, verbose_name="Продавец", on_delete=models.CASCADE,)
    category = models.IntegerField(verbose_name="Категория", choices=CATEGORIES)
    condition = models.IntegerField(verbose_name="Состояние", choices=CONDITION)
    type_announcement = models.IntegerField(verbose_name="Тип объявления", choices=TYPE_ANNOUNCEMENT)
    name = models.CharField(verbose_name="Название", max_length=50)
    price = models.DecimalField(verbose_name="Цена", max_digits=13, decimal_places=2)
    description = models.CharField(verbose_name="Описание", max_length=3000)
    sold = models.BooleanField(verbose_name="Продано", default=False)
    date_created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Дата изменения", auto_now_add=True)
    
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
    
    def __str__(self):
        return self.name if len(self.name) <= 25 else f'{self.name[0:25]}...'


def _get_announcement_sale_image_filepath(self, image_name):
    return f'user_images/{self.announcement_sale.seller.user.pk}/{self.announcement_sale.pk}/{image_name}'


class AnnouncementSaleImage(models.Model):
    announcement_sale = models.ForeignKey(AnnouncementSale, verbose_name="Объявление",  on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Изображение", upload_to=_get_announcement_sale_image_filepath)
    
    class Meta:
        verbose_name = 'Изображение объявления'
        verbose_name_plural = 'Изображения объявлений'
    
    def __str__(self):
        return self.image.name.split('/')[-1]