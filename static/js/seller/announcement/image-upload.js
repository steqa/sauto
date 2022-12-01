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
    let number = 0
    fileInputs.forEach((elem) => {
        if ([...innerFormData.keys()].includes(elem.value.split('\\').pop())) {
            formData.append(number, innerFormData.get(elem.value.split('\\').pop()))
            number += 1
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
            console.log(data)
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
