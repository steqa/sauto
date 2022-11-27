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
    for (let i = 0; i < elems.length; i++) {
        if ((elems[i].nodeName != 'BUTTON') & (elems[i].hasAttribute('data-exclude-getFormData') === false)) {
            dataArr[elems[i].name] = elems[i].value
        }
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