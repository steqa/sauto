const latitude = document.getElementById('latitude')
const longitude = document.getElementById('longitude')
ymaps.ready(init)
function init() {
    let placemark,
        map = new ymaps.Map('map', {
            center: [55.357159779610356, 86.0883104783902],
            zoom: 12
        }), mySearchControl = new ymaps.control.SearchControl({
            options: {
                noPlacemark: true
            }
        })

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
    })

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
        sendFormData(form, reload = false)
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
