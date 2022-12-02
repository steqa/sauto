const innerFormData = new FormData()
let formData = new FormData()

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

function formFile() {
    formData = new FormData()
    fileInputs.forEach((elem) => {
        if ([...innerFormData.keys()].includes(elem.value.split('\\').pop())) {
            formData.append(elem.id, innerFormData.get(elem.value.split('\\').pop()))
        }
    })
}

function sendImage(form) {
    formFile()
    formData.append('action', 'validate-image')
    let url = form.action
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
    const reader = new FileReader()
    const uploadContent = elem.querySelector('div')
    const uploadContentInput = uploadContent.querySelector('input')
    const uploadContentLabel = uploadContent.querySelector('label')
    const uploadContentDeleteButton = uploadContent.querySelector('button')
    reader.readAsDataURL(file)
    reader.onloadend = function () {
        uploadContent.style.backgroundImage = `url(${reader.result})`
        uploadContentLabel.style.display = 'none'
        uploadContentDeleteButton.style.display = 'block'
    }
    uploadContentDeleteButton.addEventListener('click', () => {
        uploadContentInput.value = ''
        uploadContent.style.backgroundImage = ''
        uploadContentLabel.style.display = 'block'
        uploadContentDeleteButton.style.display = 'none'
        deleteFile(file)
        sendImage(form)
    })
}

function imageChangeValidationStatusField(data, field) {
    console.log(data)
    const invalidFeedbackBlock = field.closest('.field-block').querySelector('.image-invalid-feedback')
    const uploadContainerContent = field.closest('.upload-container-content')
    console.log(uploadContainerContent)
    if (field.id in data['body']) {
        invalidFeedbackBlock.style.display = 'block'
        invalidFeedbackBlock.innerHTML = data['body'][field.id].join("<br>")
        uploadContainerContent.classList.remove('image-is-valid')
        uploadContainerContent.classList.add('image-is-invalid')
    } else {
        invalidFeedbackBlock.style.display = 'none'
        invalidFeedbackBlock.innerHTML = ''
        uploadContainerContent.classList.remove('image-is-invalid')
        uploadContainerContent.classList.add('image-is-valid')
    }
}