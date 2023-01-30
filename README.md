Sauto - сайт площадка для размещения объявлений
<br>
<br>
[Перейти на сайт](http://sauto.herokuapp.com/ "http://sauto.herokuapp.com/")
-------------------------

<br>

## Основной функционал:

### 1\. Регистрация, аутентификация и авторизация
1. Система предусматривает два типа пользователей: продавец и покупатель
2. Регистрация включает подтверждение адреса электронной почты
3. Реализована возможность восстановления пароля

### 2\. Функционал покупателя
1. Редактирование данных профиля:
  * Изображение
  * Имя
  * Фамилия
  * Адрес электронной почты
  * Номер телефона
  * Имя пользователя telegram
  * Пароль
2. Просмотр контактной информации продавца
3. Добавление или удаление объявления из избранного
4. Просмотр объявлений конкретного продавца в его профиле

### 3\. Функционал продавца
1. Возможность включить telegram уведомления
2. Размещение объявлений. При размещении указывается следующая информация:
  * Категория
  * Состояние
  * Тип объявления
  * Название
  * Цена
  * Описание (необязательно)
  * Изображения (от 1 до 8)
  * Местоположения. Реализовано при помощи Yandex.Maps API
  * Способ связи (1 из 3):
    * Адрес электронной почты
    * Имя пользователя telegram
    * Номер телефона
3. Редактирование объявлений
4. Удаление объявлений
5. Возможность обозначить свое объявление проданным или не проданным. Проданные объявления отображаются только в профиле продавца
6. Весь функционал покупателя
> Telegram уведомления - сообщения от telegram бота продавцу, при добавлении или удалении пользователями объявления, размещённого этим продавцом.
> <br><br>
> Пример сообщения:
> <br><br>
> <image src="https://i.imgur.com/nbiKlza.png" alt="...">

### Пользователь получает статус продавца в следующих случаях: <br>
1. После размещения первого объявления <br>
2. После указания номера телефона в настройках профиля <br>
3. После указания имени телеграм в настройках профиля

<br>

## Стек технологий:

### Backend:
<img src="https://camo.githubusercontent.com/9c181e3ed635e6db0b2dc19453cfc88e50af278cb123c84c11b09f9f4adb45c8/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d3330333633643f7374796c653d666c61742d737175617265266c6f676f3d507974686f6e266c6f676f436f6c6f723d336237376138" alt="Python" data-canonical-src="https://img.shields.io/badge/Python-30363d?style=flat-square&amp;logo=Python&amp;logoColor=3b77a8" style="max-width: 100%;">
<img src="https://camo.githubusercontent.com/d40c56b3e5360cbe771d21643ef7127db29aa15997fa6c15564e0864008958e8/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446a616e676f2d3330333633643f7374796c653d666c61742d737175617265266c6f676f3d446a616e676f266c6f676f436f6c6f723d326261393737" alt="Django" data-canonical-src="https://img.shields.io/badge/Django-30363d?style=flat-square&amp;logo=Django&amp;logoColor=2ba977" style="max-width: 100%;">
<img src="https://camo.githubusercontent.com/dbabcec23405dc109535107173f35e212cc259496d773cd25ab52de478ee7dae/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f53514c6974652d3330333633643f7374796c653d666c61742d737175617265266c6f676f3d53514c697465266c6f676f436f6c6f723d303037353866" alt="SQLite" data-canonical-src="https://img.shields.io/badge/SQLite-30363d?style=flat-square&amp;logo=SQLite&amp;logoColor=00758f" style="max-width: 100%;">

### Frontend:
<img src="https://camo.githubusercontent.com/50ad74af04b3dd60185485a45dd7fe13f767b9f32b7ec261707dca56ea0e55fe/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f48544d4c2d3330333633643f7374796c653d666c61742d737175617265266c6f676f3d48544d4c35266c6f676f436f6c6f723d653434643236" alt="HTML" data-canonical-src="https://img.shields.io/badge/HTML-30363d?style=flat-square&amp;logo=HTML5&amp;logoColor=e44d26" style="max-width: 100%;">
<img src="https://camo.githubusercontent.com/6a31aa43e254a3e99adcd5da8937d979eb4b26b431bc484150d19bcaf071d082/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4353532d3330333633643f7374796c653d666c61742d737175617265266c6f676f3d43535333266c6f676f436f6c6f723d323936356631" alt="CSS" data-canonical-src="https://img.shields.io/badge/CSS-30363d?style=flat-square&amp;logo=CSS3&amp;logoColor=2965f1" style="max-width: 100%;">
<img src="https://camo.githubusercontent.com/14125623d118f85107b908c9348bf80aeff8013858e70e7ad6d494ee4c24528c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4a6176615363726970742d3330333633643f7374796c653d666c61742d737175617265266c6f676f3d4a617661536372697074266c6f676f436f6c6f723d663764663165" alt="JavaScript" data-canonical-src="https://img.shields.io/badge/JavaScript-30363d?style=flat-square&amp;logo=JavaScript&amp;logoColor=f7df1e" style="max-width: 100%;">

### Используемые API:
#### Yandex.Maps API
#### Telegram Bot API

<br>

## Изображения:

### Главная страница
<image src="https://i.imgur.com/vsaeihF.png" alt="...">

### Просмотр объявления
<image src="https://i.imgur.com/UG14zCu.png" alt="...">

### Просмотр объявлений пользователя
<image src="https://i.imgur.com/WiF9wgP.png" alt="...">

### Вход
<image src="https://i.imgur.com/0mnIhzj.png" alt="...">

### Регистрация
<image src="https://i.imgur.com/54EGTbn.png" alt="...">

### Создание объявления (страница редактирования объявления выглядит подобным образом)
<image src="https://i.imgur.com/3cDG4nK.png" alt="...">

### Редактирование профиля
<image src="https://i.imgur.com/haEvao4.png" alt="...">
<image src="https://i.imgur.com/ixIP8Vi.png" alt="...">
