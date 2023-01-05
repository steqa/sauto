const form = document.querySelector('#edit_announcement_form')
const imageFields = document.querySelector('.imageFields').querySelectorAll('input')

const listenerAction = 'edit-announcement'

const locationData = document.querySelector('.location-data')
document.getElementById('id_latitude').value = locationData.dataset.latitude.replace(',', '.')
document.getElementById('id_longitude').value = locationData.dataset.longitude.replace(',', '.')

const communicationMethodValue = document.querySelector('.communivation-method-value')
communicationMethod.value = communicationMethodValue.dataset.communicationMethodValue

const InitialimageFields = document.querySelector('.imageFields').querySelectorAll('input.initial-image')
InitialimageFields.forEach((element) => {
    async function getFileFromUrl(url, name) {
        try {
            const response = await fetch(url)
            const data = await response.blob()
            const metadata = {
                type: 'image/jpeg'
            }
            return new File([data], name, metadata)
        } catch (error) {
            console.log(error)
        }
    }
    getFileFromUrl(element.src, element.name)
        .then((file) => {
            inputType = 'input'
            inputField = element

            const dt = new DataTransfer();
            dt.items.add(file);
            element.files = dt.files
            element.dataset.fileName = file.name

            const imgPreview = element.parentNode.querySelector('.img-preview')
            imgPreview.src = element.dataset.path
            const uploadContent = element.parentNode.parentNode.querySelector('div')
            const uploadContentLabel = uploadContent.querySelector('label')
            const uploadContentDeleteButton = uploadContent.querySelector('button')
            uploadContentLabel.style.display = 'none'
            uploadContentDeleteButton.style.display = 'block'
            const uploadContainerContent = element.closest('.upload-container-content')
            uploadContainerContent.classList.remove('image-is-invalid')
            uploadContainerContent.classList.add('image-is-valid')

            appendFile(file)
        })
})

announcementFields.forEach((element) => {
    element.classList.add('is-valid')
})