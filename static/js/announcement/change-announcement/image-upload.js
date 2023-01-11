dropArea = document.querySelectorAll('#upload-container')
fileInputs = document.querySelectorAll('[data-image-upload-input]')

dropArea.forEach((elem) => {
    elem.addEventListener('dragover', (e) => {
        e.preventDefault();
    })
    elem.addEventListener('drop', (e) => {
        if (elem.tagName == 'INPUT') {
            elem = elem.closest('#upload-container')
        } else {
            elem = elem
        }
        e.preventDefault();
        inputType = 'input'
        inputField = elem.querySelector('input')
        const inputName = elem.querySelector('[data-image-upload-input]').getAttribute('name')
        form.querySelector(`[name="${inputName}"]`).files = e.dataTransfer.files
        file = e.dataTransfer.files[0]
        inputField.dataset.fileName = file.name
        previewFile(file, elem)
        appendFile(file)
        sendImage(form, elem = inputField)
    })
})

fileInputs.forEach((elem) => {
    elem.addEventListener('input', (e) => {
        inputType = 'input'
        inputField = elem
        file = elem.files[0]
        inputField.dataset.fileName = file.name
        previewFile(file, elem.parentNode.parentNode)
        appendFile(file)
        sendImage(form, elem = inputField)
    })
})


innerFormData = new FormData()
formData = new FormData()

function appendFile(file) {
    innerFormData.append(file.name, file)
}

function deleteFile(file) {
    let quantity = 0
    for (const f of innerFormData.keys()) {
        if (file.name == f) {
            quantity += 1
        }
    }
    if (quantity > 1) {
        innerFormData.delete(file.name)
        while (quantity > 1) {
            innerFormData.append(file.name, file)
            quantity -= 1
        }
    } else {
        innerFormData.delete(file.name)
    }
}

function formFiles() {
    formData = new FormData()
    fileInputs.forEach((elem) => {
        if ([...innerFormData.keys()].includes(elem.dataset.fileName)) {
            formData.append(elem.id, innerFormData.get(elem.dataset.fileName))
        }
    })
}

function formFile(elem) {
    formData = new FormData()
    if ([...innerFormData.keys()].includes(elem.dataset.fileName)) {
        formData.append(elem.id, innerFormData.get(elem.dataset.fileName))
    }
}

function sendImage(form, reload = false, elem = null) {
    if (elem == null) {
        formFiles()
    } else {
        formFile(elem)
    }
    formData.append('action', 'validate-image')
    let url = form.action
    if (reload == true) {
        url += '?reload=true'
    }
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            renderReturnedData(data)
        })
}

function previewFile(file, elem) {
    const uploadContent = elem.querySelector('div')
    const uploadContentLabel = uploadContent.querySelector('label')
    const uploadContentDeleteButton = uploadContent.querySelector('button')
    const reader = new FileReader()
    reader.addEventListener("load", () => {
        uploadContent.style.backgroundImage = `url(${reader.result})`
        uploadContentLabel.style.display = 'none'
        uploadContentDeleteButton.style.display = 'block'
    })
    reader.readAsDataURL(file)
}

uploadContainers = document.querySelectorAll('#upload-container')
uploadContainers.forEach((element) => {
    const uploadContentDeleteButton = element.querySelector('.upload-container-content button')
    uploadContentDeleteButton.addEventListener('click', () => {
        const uploadContent = element.querySelector('div')
        const uploadContentInput = element.querySelector('input')
        const uploadContentLabel = element.querySelector('label')
        deleteFile(element.querySelector('input').files[0])
        sendImage(form, elem = element.querySelector('input'))
        uploadContentInput.value = ''
        uploadContent.style.backgroundImage = ''
        uploadContentLabel.style.display = 'block'
        uploadContentDeleteButton.style.display = 'none'
        const imgPreview = element.querySelector('.img-preview')
        if (imgPreview) {
            imgPreview.remove()
        }
    })
})

function imageChangeValidationStatusField(data, field) {
    const invalidFeedbackBlock = field.closest('.field-block').querySelector('.p-invalid-feedback')
    const uploadContainerContent = field.closest('.upload-container-content')
    const imagesInvalid = document.querySelector('.imagesInvalid')
    if (field.id in data['body']) {
        invalidFeedbackBlock.style.display = 'block'
        invalidFeedbackBlock.innerHTML = data['body'][field.id].join("<br>")
        uploadContainerContent.classList.remove('image-is-valid')
        uploadContainerContent.classList.add('image-is-invalid')
    } else if (!(field.id in data['body']) & !(field.value == '')) {
        invalidFeedbackBlock.style.display = 'none'
        invalidFeedbackBlock.innerHTML = ''
        uploadContainerContent.classList.remove('image-is-invalid')
        uploadContainerContent.classList.add('image-is-valid')
        if (typeof imagesInvalid !== "undefined" && imagesInvalid !== null) {
            imagesInvalid.style.display = 'none'
            imagesInvalid.innerHTML = ''
        }
    } else {
        invalidFeedbackBlock.style.display = 'none'
        invalidFeedbackBlock.innerHTML = ''
        uploadContainerContent.classList.remove('image-is-invalid')
        uploadContainerContent.classList.remove('image-is-valid')
    }

    if ((inputType == 'submit') & (typeof imagesInvalid !== "undefined" && imagesInvalid !== null)) {
        if ('images' in data['body']) {
            imagesInvalid.style.display = 'block'
            imagesInvalid.innerHTML = data['body']['images']
        } else {
            imagesInvalid.style.display = 'none'
            imagesInvalid.innerHTML = ''
        }
    }
}