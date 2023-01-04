const form = document.querySelector('#edit_announcement_form')
const imageFields = document.querySelector('.imageFields').querySelectorAll('input')

const listenerAction = 'edit-announcement'

const locationData = document.querySelector('.location-data')
document.getElementById('id_latitude').value = locationData.dataset.latitude.replace(',', '.')
document.getElementById('id_longitude').value = locationData.dataset.longitude.replace(',', '.')

const communicationMethodValue = document.querySelector('.communivation-method-value')
communicationMethod.value = communicationMethodValue.dataset.communicationMethodValue