const changeModal = document.querySelector('.change-modal')
const changeModalTitle = changeModal.querySelector('h1')
const changeModalSubmitBtn = changeModal.querySelector('button[type="submit"]')
const form = changeModal.querySelector('form')
const changeBtns = document.querySelectorAll('.change-btn')
const changeInputDiv = document.querySelector('.change-input-div')

let changeModalInputs = null
let inputType = null
let inputField = null

changeBtns.forEach((element) => {
    element.addEventListener('click', (e) => {
        changeModalTitle.innerHTML = element.dataset.modalTitle
        let changeInput = null
        if (element.dataset.modalInputName == 'phone_number') {
            changeInput = document.querySelector('.phone_number')
            const inputHidden = changeInput.querySelector('input[type="hidden"]')
            const inputCountryCode = changeInput.querySelector('select')
            const inputCountryCodeOptions = inputCountryCode.querySelectorAll('option')
            for (let i = 0; i < inputCountryCodeOptions.length; i++) {
                if (inputCountryCodeOptions[i].value === inputHidden.dataset.phoneNumberCountryCode) {
                    inputCountryCodeOptions[i].setAttribute("selected", "true")
                } else {
                    inputCountryCodeOptions[i].removeAttribute("selected")
                }
            }
            const inputNumber = changeInput.querySelector('input')
            inputNumber.value = inputHidden.dataset.phoneNumberWithoutCountrCode
            changeModalSubmitBtn.dataset.action = 'change-seller-data'
        } else if (element.dataset.modalInputName == 'telegram_username') {
            changeInput = document.querySelector('.telegram_username')
            const input = changeInput.querySelector('input')
            input.value = element.dataset.modalInputValue
            changeModalSubmitBtn.dataset.action = 'change-seller-data'
        } else if (element.dataset.modalInputName == 'password') {
            changeInput = document.querySelector('.new_password')
            changeModalSubmitBtn.dataset.action = 'change-user-password'
        } else if (element.dataset.modalInputName == 'image') {
            changeInput = document.querySelector('.new_image')
            changeModalSubmitBtn.dataset.action = 'validate-image'
            document.querySelector(`[src="${element.dataset.src}"]`).remove()
            const script = document.createElement('script')
            script.src = element.dataset.src
            document.documentElement.appendChild(script)
        } else {
            changeInput = document.querySelector('.change_input')
            const input = changeInput.querySelector('input')
            input.type = element.dataset.modalInputType
            input.name = element.dataset.modalInputName
            input.value = element.dataset.modalInputValue
            changeModalSubmitBtn.dataset.action = 'change-user-data'
        }
        changeInputDiv.innerHTML = ''
        changeInputDiv.append(changeInput.cloneNode(true))
        changeModalInputs = changeInputDiv.querySelectorAll('select, input')
        changeModalInputs.forEach((input) => {
            if (element.dataset.modalInputName == 'image') {
                removeErrorFileField(input)
            } else {
                removeErrorField(input)
            }
        })
        changeModalInputsListener(element)
    })
})

function changeModalInputsListener(changeBtn) {
    changeModalInputs.forEach((element) => {
        element.addEventListener('input', (e) => {
            inputType = 'input'
            inputField = element
            if (changeBtn.dataset.modalInputValue == element.value) {
                displayErrorUnchangedField(inputField)
            } else if (element.value == '') {
                displayErrorEmptyField(inputField)
            } else {
                if (inputField.type == 'file') {
                } else {
                    sendJsonFormData(changeModalInputs, reload = false, action = changeModalSubmitBtn.dataset.action)
                }
            }
        })

        form.addEventListener('submit', (e) => {
            e.preventDefault()
            inputType = 'submit'
            inputField = element
            if (changeBtn.dataset.modalInputValue == element.value) {
                displayErrorUnchangedField(inputField)
            } else if (element.value == '') {
                if (inputField.type == 'file') {
                    displayErrorEmptyFileField(inputField)
                } else {
                    displayErrorEmptyField(inputField)
                }
            } else {
                if (inputField.type == 'file') {
                    sendImage(form, reload = true, inputField)
                } else {
                    sendJsonFormData(changeModalInputs, reload = true, action = changeModalSubmitBtn.dataset.action)
                }
            }
        })
    })
}

function renderReturnedData(data) {
    if (data['type'] == 'ImageValidationError') {
        fileInputs.forEach((field) => {
            imageChangeValidationStatusField(data, field = field)
        })
    } else {
        if (data['status'] == 400) {
            if (data['type'] == 'ValidationError') {
                if (inputField.name in data['body']) {
                    if (('phone_number_0', 'phone_number_1').includes(inputField.name)) {
                        changeModalInputs.forEach((input) => {
                            displayErrorField(data['body'][input.name], input)
                        })
                    }
                    displayErrorField(data['body'][inputField.name], inputField)
                } else {
                    displaySuccessField(inputField)
                }
            } else if (data['type'] == 'BadRequest') {
                return showToast(data['body']['error'], type = 'error')
            }
        } else if (data['status'] == 200) {
            if (inputType == 'input') {
                changeModalInputs.forEach((input) => {
                    displaySuccessField(input)
                })
            } else if (inputType == 'submit') {
                removeErrorField(inputField)
                changeModalJs.hide()
                localStorage.setItem('status', data['status'])
                localStorage.setItem('message', data['body']['success'])
                window.location.replace(data['body']['url'])
            }
        }
    }
}

function displayErrorUnchangedField(field) {
    field.classList.remove('is-valid')
    field.classList.add('is-invalid')
    fieldBlock = field.closest('.field-block')
    fieldErrorBlock = fieldBlock.querySelector('.invalid-feedback')
    fieldErrorBlock.innerHTML = 'Вы ничего не изменили.'
}

function displayErrorEmptyField(field) {
    field.classList.remove('is-valid')
    field.classList.add('is-invalid')
    fieldBlock = field.closest('.field-block')
    fieldErrorBlock = fieldBlock.querySelector('.invalid-feedback')
    fieldErrorBlock.innerHTML = 'Обязательное поле.'
}

function displayErrorEmptyFileField(field) {
    const invalidFeedbackBlock = field.closest('.field-block').querySelector('.p-invalid-feedback')
    const uploadContainerContent = field.closest('.upload-container-content')
    invalidFeedbackBlock.style.display = 'block'
    invalidFeedbackBlock.innerHTML = 'Обязательное поле.'
    uploadContainerContent.classList.remove('image-is-valid')
    uploadContainerContent.classList.add('image-is-invalid')
}

function removeErrorField(field) {
    field.classList.remove('is-invalid')
    field.classList.remove('is-valid')
    fieldBlock = field.closest('.field-block')
    fieldErrorBlock = fieldBlock.querySelector('.invalid-feedback')
    fieldErrorBlock.innerHTML = ''
}

function removeErrorFileField(field) {
    field.value = ''
    const uploadContainer = field.closest('.field-block')
    const invalidFeedbackBlock = uploadContainer.querySelector('.p-invalid-feedback')
    invalidFeedbackBlock.style.display = 'none'
    invalidFeedbackBlock.innerHTML = ''
    const uploadContainerContent = uploadContainer.querySelector('.upload-container-content')
    uploadContainerContent.classList.remove('image-is-invalid')
    uploadContainerContent.classList.remove('image-is-valid')
    const uploadContentDeleteButton = uploadContainer.querySelector('.upload-container-content button')
    uploadContentDeleteButton.style.display = 'none'
    const uploadContentLabel = uploadContainer.querySelector('label')
    uploadContentLabel.style.display = 'block'
    const uploadContent = uploadContainer.querySelector('.upload-container-content')
    uploadContent.style.backgroundImage = ''
}

function displaySuccessField(field) {
    field.classList.remove('is-invalid')
    field.classList.add('is-valid')
    fieldBlock = field.closest('.field-block')
    fieldErrorBlock = fieldBlock.querySelector('.invalid-feedback')
    fieldErrorBlock.innerHTML = ''
}

function displayErrorField(error, field) {
    field.classList.remove('is-valid')
    field.classList.add('is-invalid')
    fieldBlock = field.closest('.field-block')
    fieldErrorBlock = fieldBlock.querySelector('.invalid-feedback')
    fieldErrorBlock.innerHTML = error
}