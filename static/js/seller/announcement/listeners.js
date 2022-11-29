const dropArea = document.querySelectorAll('#upload-container')
const fileInputs = document.querySelectorAll('[data-image-upload-input]')

dropArea.forEach((elem) => {
    elem.addEventListener('dragover', (e) => {
        e.preventDefault();
    })
    elem.addEventListener('drop', (e) => {
        e.preventDefault();
        const inputName = elem.querySelector('[data-image-upload-input]').getAttribute('name')
        form.querySelector(`[name="${inputName}"]`).files = e.dataTransfer.files
        file = e.dataTransfer.files[0]
        previewFile(file, elem)
        appendFile(file)
        sendImage(form)
    })
})

fileInputs.forEach((elem) => {
    elem.addEventListener('input', (e) => {
        file = elem.files[0]
        previewFile(file, elem.parentNode.parentNode)
        appendFile(file)
        sendImage(form)
    })
})


const announcementFields = document.querySelectorAll('.announcementFields .form-control')
const communicationMethodRadio = document.querySelectorAll('.communicationMethodRadio')

announcementFields.forEach((element) => {
    element.addEventListener('input', (e) => {
        inputType = 'input'
        inputField = element
        sendJsonFormData(announcementFields, reload = false, action = 'announcementData')
    })
})

communicationMethodRadio.forEach((element) => {
    element.addEventListener('input', (e) => {
        sendJsonFormData(announcementFields, reload = false, action = 'announcementData')
    })
})

function mapListener() {
    sendJsonFormData(announcementFields, reload = false, action = 'announcementData')
}


const sellerFields = document.querySelectorAll('.sellerFields .form-control, .sellerFields .form-select')

sellerFields.forEach((element) => {
    element.addEventListener('input', (e) => {
        inputType = 'input'
        inputField = element
        sendJsonFormData(sellerFields, reload = false, action = 'sellerData')
    })
})

function formFormData() {
    const formData = new FormData()
    formData.append('action', 'addAnnouncement')
    announcementFields.forEach((element) => {
        formData.append(element.name, element.value)
    })
    let number = 0
    fileInputs.forEach((elem) => {
        if ([...innerFormData.keys()].includes(elem.value.split('\\').pop())) {
            formData.append(number, innerFormData.get(elem.value.split('\\').pop()))
            number += 1
        }
    })
    sellerFields.forEach((element) => {
        formData.append(element.name, element.value)
    })
    return formData
}

form.addEventListener('submit', (e) => {
    e.preventDefault()
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