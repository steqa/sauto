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

    function getAddress(coords) {
        ymaps.geocode(coords).then(function (res) {
            const firstGeoObject = res.geoObjects.get(0)
            const address = firstGeoObject.getAddressLine()
            const addressContainer = document.getElementById('addressContainer')
            addressContainer.innerHTML = address
        })
    }
    getAddress([latitude, longitude])

    const mapLoaderSpiner = document.querySelector('.map-loader-spiner')
    mapLoaderSpiner.style.display = 'none'

    map.geoObjects.add(placemark)
    map.controls.remove('geolocationControl')
    map.controls.remove('searchControl')
    map.controls.remove('trafficControl')
    map.controls.remove('typeSelector')
    map.controls.remove('fullscreenControl')
    map.controls.remove('zoomControl')
    map.controls.remove('rulerControl')
}