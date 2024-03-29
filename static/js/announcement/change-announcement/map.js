const latitude = document.getElementById('id_latitude')
const longitude = document.getElementById('id_longitude')
ymaps.ready(init)
function init() {
    let placemark, map = null
    if (listenerAction == 'edit-announcement') {
        const latitude = document.getElementById('map').dataset.latitude.replace(',', '.')
        const longitude = document.getElementById('map').dataset.longitude.replace(',', '.')
        placemark, map = new ymaps.Map('map', {
            center: [latitude, longitude],
            zoom: 12
        }), mySearchControl = new ymaps.control.SearchControl({
            options: {
                noPlacemark: true
            }
        })
    } else if (listenerAction == 'add-announcement') {
        placemark, map = new ymaps.Map('map', {
            center: [55.357159779610356, 86.0883104783902],
            zoom: 12
        }), mySearchControl = new ymaps.control.SearchControl({
            options: {
                noPlacemark: true
            }
        })
    }

    // Убираем добавление метки при поиске
    map.controls.add(mySearchControl)
    mySearchControl.events.add('submit', function (e) {
    })

    // Слушаем клик на карте.
    map.events.add('click', function (e) {
        const coords = e.get('coords')

        // Если метка уже создана – просто передвигаем ее.
        if (placemark) {
            placemark.geometry.setCoordinates(coords)
        }
        // Если нет – создаем.
        else {
            placemark = createPlacemark(coords)
            map.geoObjects.add(placemark)
            // Слушаем событие окончания перетаскивания на метке.
            placemark.events.add('dragend', function () {
                getAddress(placemark.geometry.getCoordinates())
            })
        }
        getAddress(coords)
        mapListener()
    })

    // Если координаты имеются сразу после загрузки страницы - создаём метку.
    if ((latitude.value != '') & (longitude.value != '')) {
        coords = [Number(latitude.value), Number(longitude.value)]
        placemark = createPlacemark(coords)
        map.geoObjects.add(placemark)
        getAddress(coords)
    }


    // Создание метки.
    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'Поиск...'
        }, {
            preset: 'islands#blueDotIconWithCaption',
            draggable: true
        })
    }

    // Определяем адрес по координатам (обратное геокодирование).
    function getAddress(coords) {
        placemark.properties.set('iconCaption', 'Поиск...')
        ymaps.geocode(coords).then(function (res) {
            const firstGeoObject = res.geoObjects.get(0)

            placemark.properties
                .set({
                    // Формируем строку с данными об объекте.
                    iconCaption: [
                        // Название населенного пункта или вышестоящее административно-территориальное образование.
                        firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas(),
                        // Получаем путь до топонима, если метод вернул null, запрашиваем наименование здания.
                        firstGeoObject.getThoroughfare() || firstGeoObject.getPremise()
                    ].filter(Boolean).join(', '),
                    // В качестве контента балуна задаем строку с адресом объекта.
                    balloonContent: firstGeoObject.getAddressLine()
                })
        })

        latitude.value = coords[0]
        longitude.value = coords[1]
    }

    // Убираем элементы управления с карты
    map.controls.remove('geolocationControl')
    map.controls.remove('searchControl')
    map.controls.remove('trafficControl')
    map.controls.remove('typeSelector')
    map.controls.remove('fullscreenControl')
    map.controls.remove('zoomControl')
    map.controls.remove('rulerControl')
}


function locationChangeValidationStatusField(data) {
    if (('latitude' in data['body']) || ('longitude' in data['body'])) {
        document.querySelector('.locationInvalid').style.display = 'block'
    } else {
        document.querySelector('.locationInvalid').style.display = 'none'
    }
}
