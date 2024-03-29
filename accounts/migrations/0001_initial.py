# Generated by Django 4.1.3 on 2023-01-16 11:35

import accounts.managers
import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=260, unique=True, verbose_name='адрес электронной почты')),
                ('first_name', models.CharField(max_length=150, verbose_name='имя')),
                ('last_name', models.CharField(max_length=150, verbose_name='фамилия')),
                ('profile_image', models.ImageField(blank=True, default=accounts.models._get_default_profile_image, null=True, upload_to=accounts.models._get_profile_image_filepath, verbose_name='изображение профиля')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='последний вход')),
                ('is_active', models.BooleanField(default=True, verbose_name='активный')),
                ('is_staff', models.BooleanField(default=False, verbose_name='статус персонала')),
                ('is_admin', models.BooleanField(default=False, verbose_name='статус администратора')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='статус суперпользователя')),
                ('is_email_verified', models.BooleanField(default=False, verbose_name='статус проверенной электронной почты')),
                ('last_password_updated', models.DateTimeField(auto_now=True, verbose_name='последнее обновление пароля')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
            managers=[
                ('objects', accounts.managers.UserManager()),
            ],
        ),
    ]
