const announcementFields = document.querySelectorAll('.announcementFields .form-control')
const communicationMethodRadio = document.querySelectorAll('.communicationMethodRadio')

announcementFields.forEach((element) => {
    element.addEventListener('input', (e) => {
        inputType = 'input'
        inputField = element
        sendJsonFormData(announcementFields, reload = false, action = 'validate-announcement-data')
    })
})

communicationMethodRadio.forEach((element) => {
    element.addEventListener('input', (e) => {
        inputField = 'communicationMethod'
        sendJsonFormData(announcementFields, reload = false, action = 'validate-announcement-data')
    })
})

const locationFields = document.querySelector('.locationFields').querySelectorAll('input')

function mapListener() {
    inputField = 'location'
    inputType = 'input'
    sendJsonFormData(locationFields, reload = false, action = 'validate-announcement-data')
}


const sellerFields = document.querySelectorAll('.sellerFields .form-control, .sellerFields .form-select')

sellerFields.forEach((element) => {
    element.addEventListener('input', (e) => {
        inputType = 'input'
        inputField = element
        sendJsonFormData(sellerFields, reload = false, action = 'validate-seller-data')
    })
})

function formFormData() {
    const formData = new FormData()
    formData.append('action', listenerAction)
    announcementFields.forEach((element) => {
        formData.append(element.name, element.value)
    })
    let number = 0
    fileInputs.forEach((element) => {
        if ([...innerFormData.keys()].includes(element.dataset.fileName)) {
            formData.append(number, innerFormData.get(element.dataset.fileName))
            number += 1
        }
    })
    sellerFields.forEach((element) => {
        formData.append(element.name, element.value)
    })
    locationFields.forEach((element) => {
        formData.append(element.name, element.value)
    })
    return formData
}

form.addEventListener('submit', (e) => {
    e.preventDefault()
    inputType = 'submit'
    formData = formFormData()
    const url = form.action + '?reload=true'
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData,
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            renderReturnedData(data)
        })
})