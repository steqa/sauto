from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from seller.models import Seller


class Announcement(models.Model):
    CATEGORIES = (
        (None, 'Не выбрано'),
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
        (None, 'Не выбрано'),
        (0, 'БУ'),
        (1, 'Новое')
    )
    
    TYPE_ANNOUNCEMENT = (
        (None, 'Не выбрано'),
        (0, 'Продаю свое'),
        (1, 'Приобрел на продажу'),
        (2, 'Магазин'),
    )
    
    COMMUNICATION_METHOD = (
        (0, 'Адрес электронной почты'),
        (1, 'Имя пользователя телеграм'),
        (2, 'Номер телефона')
    )
    
    seller = models.ForeignKey(Seller, verbose_name="продавец", on_delete=models.CASCADE)
    category = models.IntegerField(verbose_name="категория", choices=CATEGORIES)
    condition = models.IntegerField(verbose_name="состояние", choices=CONDITION)
    type_announcement = models.IntegerField(verbose_name="тип объявления", choices=TYPE_ANNOUNCEMENT)
    name = models.CharField(verbose_name="название", max_length=50)
    price = models.DecimalField(verbose_name="цена", max_digits=13, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(verbose_name="описание", max_length=3000, blank=True, null=True)
    sold = models.BooleanField(verbose_name="продано", default=False)
    latitude = models.FloatField(verbose_name="широта")
    longitude = models.FloatField(verbose_name="долгота")
    date_created = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="дата изменения", auto_now_add=True)
    communication_method = models.IntegerField(verbose_name="способ связи", choices=COMMUNICATION_METHOD, default=0)
    
    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'
        ordering = ('-date_created', )
    
    def __str__(self):
        return self.name if len(self.name) <= 25 else f'{self.name[0:25]}...'


def _get_announcement_sale_image_filepath(self, image_name):
    return f'user_images/{self.announcement.seller.user.pk}/{self.announcement.pk}/{image_name}'


class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(Announcement, verbose_name="объявление",  on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="изображение", upload_to=_get_announcement_sale_image_filepath)
    
    class Meta:
        verbose_name = 'изображение объявления'
        verbose_name_plural = 'изображения объявлений'
    
    def __str__(self):
        return self.image.name.split('/')[-1]
    
    def delete(self):
        self.image.storage.delete(self.image.name)
        super().delete()