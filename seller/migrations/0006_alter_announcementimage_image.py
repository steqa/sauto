# Generated by Django 4.1.3 on 2022-12-01 09:55

from django.db import migrations, models
import seller.models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0005_rename_announcement_sale_announcementimage_announcement_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcementimage',
            name='image',
            field=models.ImageField(upload_to=seller.models._get_announcement_sale_image_filepath, verbose_name='изображение'),
        ),
    ]
