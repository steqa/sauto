const fullscreenMapContainer = document.querySelector('.fullscreen-map-container')
const fullscreenMapContainerBtnClose = document.querySelector('.fullscreen-map-btn-close')
const mapContainer = document.querySelector('.show-map-container')

const latitude = document.getElementById('map').dataset.latitude.replace(',', '.')
const longitude = document.getElementById('map').dataset.longitude.replace(',', '.')

mapContainer.addEventListener('click', () => {
    createFullScreenMap()
    fullscreenMapContainer.style.display = 'flex'
})

fullscreenMapContainerBtnClose.addEventListener('click', () => {
    fullscreenMapContainer.style.display = 'none'
})

fullscreenMapContainer.addEventListener('click', (e) => {
    if (e.target == fullscreenMapContainer) {
        fullscreenMapContainer.style.display = 'none'
    }
})

function createFullScreenMap() {
    const loadedMap = document.getElementById('loadedMap')
    const map = document.getElementById('map')
    loadedMap.innerHTML = ''
    loadedMap.id = 'map'
    map.id = 'loadedMap'
    init()
    loadedMap.id = 'loadedMap'
    map.id = 'map'
}