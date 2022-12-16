ymaps.ready(init)
function init() {
    const latitude = document.getElementById('map').dataset.latitude.replace(',', '.')
    const longitude = document.getElementById('map').dataset.longitude.replace(',', '.')
    const map = new ymaps.Map('map', {
        center: [latitude, longitude],
        zoom: 15,
        draggable: false,
    })

    const placemark = new ymaps.Placemark([latitude, longitude], {}, {
        preset: 'islands#blueDotIcon',
    })

    map.geoObjects.add(placemark)
    map.controls.remove('geolocationControl')
    map.controls.remove('searchControl')
    map.controls.remove('trafficControl')
    map.controls.remove('typeSelector')
    map.controls.remove('fullscreenControl')
    map.controls.remove('zoomControl')
    map.controls.remove('rulerControl')
}