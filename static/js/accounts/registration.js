const registrationForm = document.querySelector('#registration_form')
const formFields = document.querySelectorAll('.form-control')

let inputType = null
let inputField = null

registrationForm.addEventListener('submit', function (e) {
    e.preventDefault()
    inputType = 'submit'
    sendFormData(this, reload = true)
})

formFields.forEach((element) => {
    element.addEventListener('input', function (e) {
        inputType = 'input'
        inputField = element
        sendFormData(registrationForm, reload = false)
    })
})


function getFormData(e) {
    const elems = e.elements,
        dataArr = new Object;
    for (let i = 0; i < elems.length - 1; i++) {
        dataArr[elems[i].name] = elems[i].value
    }
    return dataArr
}


function sendFormData(e, reload) {
    const formData = getFormData(e)
    const url = e.action
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            'formData': formData,
            'reload': reload
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            if (data['status'] == 400) {
                if (data['type'] == 'BadRequest') {
                    return showError(data['error'])
                } else if (data['type'] == 'ValidationError') {
                    if (inputType == 'submit') {
                        formFields.forEach((field) => {
                            changeValidationStatusField(data, field)
                        })
                    } else {
                        const field = inputField
                        changeValidationStatusField(data, field)
                    }
                }
            } else if (data['status'] == 200) {
                if (data['redirect']) {
                    window.location.replace(data['redirect'])
                } else {
                    formFields.forEach((field) => {
                        changeValidationStatusField(data, field)
                    })
                }
            }
        })
}


function changeValidationStatusField(data, field) {
    const invalidFeedbackBlock = field.closest('.field-block').querySelector('.invalid-feedback')
    const fieldName = field.getAttribute('name')
    if (data['error']) {
        if (fieldName in data['error']) {
            fieldInvalid(field)
        } else {
            fieldValid(field)
        }
    } else {
        fieldValid(field)
    }

    function fieldInvalid(field) {
        field.classList.remove('is-valid')
        field.classList.add('is-invalid')
        invalidFeedbackBlock.innerHTML = data['error'][fieldName].join("<br>")
    }

    function fieldValid(field) {
        field.classList.remove('is-invalid')
        field.classList.add('is-valid')
        invalidFeedbackBlock.innerHTML = ''
    }
}


function showError(error) {
    const errorToast = document.getElementById('errorToast')
    const errorMessage = errorToast.querySelector('.toast-body')
    errorMessage.innerHTML = error
    const toast = new bootstrap.Toast(errorToast)
    toast.show()
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}