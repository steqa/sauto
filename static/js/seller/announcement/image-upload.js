const dropArea = document.querySelectorAll('#upload-container')
const fileInputs = document.querySelectorAll('[data-image-upload-input]')
const formData = new FormData()
let returnedFormData = new FormData()

dropArea.forEach((elem) => {
    elem.addEventListener('dragover', function (e) {
        e.preventDefault();
    })
    elem.addEventListener('drop', function (e) {
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
    elem.addEventListener('input', function (e) {
        file = elem.files[0]
        previewFile(file, elem.parentNode.parentNode)
        appendFile(file)
        sendImage(form)
    })
})

function appendFile(file) {
    formData.append(file.name, file)
}

function deleteFile(file) {
    let quantity = 0
    for (const f of formData.keys()) {
        if (file.name == f) {
            quantity += 1
        }
    }
    console.log(quantity)
    if (quantity > 1) {
        formData.delete(file.name)
        while (quantity > 1) {
            formData.append(file.name, file)
            quantity -= 1
        }
    } else {
        formData.delete(file.name)
    }
}

function formFile() {
    returnedFormData = new FormData()
    let number = 0
    fileInputs.forEach((elem) => {
        if ([...formData.keys()].includes(elem.value.split('\\').pop())) {
            returnedFormData.append(number, formData.get(elem.value.split('\\').pop()))
            number += 1
        }
    })
}

function sendImage(form) {
    formFile()
    let url = form.action
    $.ajax({
        url: url,
        type: "POST",
        data: returnedFormData,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        processData: false,
        contentType: false,
        success: function (data) {
            console.log(data)
        },
        error: function (error) {
            console.log(error)
        }
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
        uploadContentInput.setAttribute('data-exclude-getFormData', true)
        uploadContentInput.value = ''
        uploadContent.style.backgroundImage = ''
        uploadContentLabel.style.display = 'block'
        uploadContentDeleteButton.style.display = 'none'
        deleteFile(file)
        sendImage(form)
    })
}
