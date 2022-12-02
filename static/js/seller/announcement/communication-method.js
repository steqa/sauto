const radios = document.querySelectorAll('.communicationMethodRadio')
const communicationMethod = document.getElementById('id_communication_method')

radios.forEach((element) => {
    element.addEventListener('click', (e) => {
        radios.forEach((elem) => {
            elem.checked = false
        })
        element.checked = true
        communicationMethod.value = element.value
    })
})

function sellerDataChangeValidationStatusField(data, field) {
    const invalidFeedbackBlock = field.closest('.field-block').querySelector('.invalid-feedback')
    const phoneNumber0 = document.getElementById('id_phone_number_0')
    const phoneNumber1 = document.getElementById('id_phone_number_1')
    if ((field.id == 'id_phone_number_0') || (field.id == 'id_phone_number_1')) {
        const radioID = phoneNumber1.parentElement.getAttribute('data-communication-method-input-id')
        const radio = document.getElementById(radioID)
        if (!(phoneNumber0.name in data['body']) & !(phoneNumber1.name in data['body'])) {
            radio.disabled = false
        } else {
            radio.disabled = true
            if (radio.checked) {
                radio.checked = false
                radios[0].checked = true
                communicationMethod.value = radios[0].value
            }
        }
    } else if (field.id == 'id_telegram_username') {
        const radioID = field.parentElement.getAttribute('data-communication-method-input-id')
        const radio = document.getElementById(radioID)
        if (!(field.name in data['body'])) {
            radio.disabled = false
        } else {
            radio.disabled = true
            if (radio.checked) {
                radio.checked = false
                radios[0].checked = true
                communicationMethod.value = radios[0].value
            }
        }
    }

    if (field.id == 'id_phone_number_1') {
        const phoneNumber0invalidFeedbackBlock = phoneNumber0.closest('.field-block').querySelector('.invalid-feedback')
        if (field.name in data['body']) {
            if (field.value == '') {
                field.classList.remove('is-valid')
                field.classList.remove('is-invalid')
                invalidFeedbackBlock.innerHTML = ''
                phoneNumber0.classList.remove('is-valid')
                phoneNumber0.classList.remove('is-invalid')
                phoneNumber0invalidFeedbackBlock.innerHTML = ''
            } else if ((field.value != '') & (phoneNumber0.value == '')) {
                field.classList.remove('is-valid')
                field.classList.add('is-invalid')
                invalidFeedbackBlock.innerHTML = ''
                phoneNumber0.classList.remove('is-valid')
                phoneNumber0.classList.add('is-invalid')
                phoneNumber0invalidFeedbackBlock.innerHTML = data['body'][phoneNumber0.name].join("<br>")
            } else {
                field.classList.remove('is-valid')
                field.classList.add('is-invalid')
                invalidFeedbackBlock.innerHTML = data['body'][field.name].join("<br>")
                phoneNumber0.classList.remove('is-valid')
                phoneNumber0.classList.add('is-invalid')
                phoneNumber0invalidFeedbackBlock.innerHTML = ''
            }
        } else {
            field.classList.remove('is-invalid')
            field.classList.add('is-valid')
            invalidFeedbackBlock.innerHTML = ''
            phoneNumber0.classList.remove('is-invalid')
            phoneNumber0.classList.add('is-valid')
            phoneNumber0invalidFeedbackBlock.innerHTML = ''
        }
    } else if (field.id == 'id_phone_number_0') {
        const phoneNumber1invalidFeedbackBlock = phoneNumber1.closest('.field-block').querySelector('.invalid-feedback')
        if (phoneNumber1.value != '') {
            if (field.name in data['body']) {
                field.classList.remove('is-valid')
                field.classList.add('is-invalid')
                invalidFeedbackBlock.innerHTML = data['body'][field.name].join("<br>")
                phoneNumber1.classList.remove('is-valid')
                phoneNumber1.classList.add('is-invalid')
                phoneNumber1invalidFeedbackBlock.innerHTML = ''
            } else {
                if (phoneNumber1.name in data['body']) {
                    field.classList.remove('is-valid')
                    field.classList.add('is-invalid')
                    invalidFeedbackBlock.innerHTML = ''
                    phoneNumber1.classList.remove('is-valid')
                    phoneNumber1.classList.add('is-invalid')
                    phoneNumber1invalidFeedbackBlock.innerHTML = data['body'][phoneNumber1.name].join("<br>")
                } else {
                    field.classList.remove('is-invalid')
                    field.classList.add('is-valid')
                    invalidFeedbackBlock.innerHTML = ''
                    phoneNumber1.classList.remove('is-invalid')
                    phoneNumber1.classList.add('is-valid')
                    phoneNumber1invalidFeedbackBlock.innerHTML = ''
                }
            }
        } else {
            field.classList.remove('is-valid')
            field.classList.remove('is-invalid')
            invalidFeedbackBlock.innerHTML = ''
            phoneNumber1.classList.remove('is-valid')
            phoneNumber1.classList.remove('is-invalid')
            phoneNumber1invalidFeedbackBlock.innerHTML = ''
        }
    } else if (field.id == 'id_telegram_username') {
        if (field.value == '') {
            field.classList.remove('is-valid')
            field.classList.remove('is-invalid')
            invalidFeedbackBlock.innerHTML = ''
        } else {
            if (field.name in data['body']) {
                field.classList.remove('is-valid')
                field.classList.add('is-invalid')
                invalidFeedbackBlock.innerHTML = data['body'][field.name].join("<br>")
            } else {
                field.classList.remove('is-invalid')
                field.classList.add('is-valid')
                invalidFeedbackBlock.innerHTML = ''
            }
        }
    }
}