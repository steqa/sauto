const formFields = document.querySelectorAll('.form-control')

let inputType = null
let inputField = null

form.addEventListener('submit', function (e) {
    e.preventDefault()
    inputType = 'submit'
    sendFormData(this, reload = true)
})

formFields.forEach((element) => {
    element.addEventListener('input', function (e) {
        inputType = 'input'
        inputField = element
        sendFormData(form, reload = false)
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
    let url = e.action
    if (reload) { 
        url += '?reload=true'
    }
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            'form_data': formData,
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            renderReturnedData(data)
        })
}


function changeValidationStatusField(data, field) {
    const invalidFeedbackBlock = field.closest('.field-block').querySelector('.invalid-feedback')
    const fieldName = field.getAttribute('name')
    if (fieldName in data['body']) {
        field.classList.remove('is-valid')
        field.classList.add('is-invalid')
        invalidFeedbackBlock.innerHTML = data['body'][fieldName].join("<br>")
    } else {
        field.classList.remove('is-invalid')
        field.classList.add('is-valid')
        invalidFeedbackBlock.innerHTML = ''
    }
}


function showToast(msg, type) {
    const toast = document.getElementById('toast')
    const message = toast.querySelector('.toast-body')
    if (type == 'error') {
        toast.classList.remove('text-bg-success')
        toast.classList.add('text-bg-danger')
    } else if (type == 'success') {
        toast.classList.remove('text-bg-danger')
        toast.classList.add('text-bg-success')
    }
    message.innerHTML = msg
    const toastShow = new bootstrap.Toast(toast)
    toastShow.show()
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