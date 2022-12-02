# Generated by Django 4.1.3 on 2022-11-29 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_announcement_latitude_announcement_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='communication_method',
            field=models.IntegerField(choices=[(0, 'email'), (1, 'telegram_username'), (2, 'phone_number')], default=0, verbose_name='способ связи'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='description',
            field=models.CharField(blank=True, max_length=3000, null=True, verbose_name='описание'),
        ),
    ]