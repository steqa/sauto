const changeModal = document.querySelector('.change-modal')
const changeModalTitle = changeModal.querySelector('h1')
const changeModalSubmitBtn = changeModal.querySelector('button[type="submit"]')
const form = changeModal.querySelector('form')
const changeBtns = document.querySelectorAll('.change-btn')
const changeInputDiv = document.querySelector('.change-input-div')
let changeModalInputs = null

let inputType = null

changeBtns.forEach((element) => {
    element.addEventListener('click', (e) => {
        changeModalTitle.innerHTML = element.dataset.modalTitle
        let changeInput = null
        if (element.dataset.modalInputName == 'phone_number') {
            changeInput = document.querySelector('.phone_number')
            changeModalSubmitBtn.dataset.action = 'change-seller-data'
        } else if (element.dataset.modalInputName == 'telegram_username') {
            changeInput = document.querySelector('.telegram_username')
            const input = changeInput.querySelector('input')
            input.value = element.dataset.modalInputValue
            changeModalSubmitBtn.dataset.action = 'change-seller-data'
        } else if (element.dataset.modalInputName == 'password') {
            changeInput = document.querySelector('.change_input')
            const input = changeInput.querySelector('input')
            input.type = element.dataset.modalInputType
            input.name = element.dataset.modalInputName
            input.autocomplete = 'new-password'
            changeModalSubmitBtn.dataset.action = 'change-user-password'
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
        removeErrorField()
        changeModalInputsListener(element)
    })
})

function changeModalInputsListener(changeBtn) {
    changeModalInputs.forEach((element) => {
        element.addEventListener('input', (e) => {
            inputType = 'input'
            if (changeBtn.dataset.modalInputValue == element.value) {
                displayErrorUnchangedField()
            } else if (element.value == '') {
                displayErrorEmptyField()
            } else {
                removeErrorField()
                sendJsonFormData(changeModalInputs, reload = false, action = changeModalSubmitBtn.dataset.action)
            }
        })

        form.addEventListener('submit', (e) => {
            e.preventDefault()
            inputType = 'submit'
            if (changeBtn.dataset.modalInputValue == element.value) {
                displayErrorUnchangedField()
            } else if (element.value == '') {
                displayErrorEmptyField()
            } else {
                removeErrorField()
                sendJsonFormData(changeModalInputs, reload = true, action = changeModalSubmitBtn.dataset.action)
            }
        })
    })
}

function renderReturnedData(data) {
    if (data['status'] == 400) {
        if (data['type'] == 'ValidationError') {
            if (changeModalInputs[0].name in data['body']) {
                displayErrorField(data['body'][changeModalInputs[0].name])
            } else {
                displaySuccessField()
            }
        }
    } else if (data['status'] == 200) {
        if (inputType == 'input') {
            displaySuccessField()
        } else if (inputType == 'submit') {
            removeErrorField()
            changeModalJs.hide()
            localStorage.setItem('status', data['status'])
            localStorage.setItem('message', data['body']['success'])
            window.location.replace(data['body']['url'])
        }
    }
}

function displayErrorUnchangedField() {
    changeModalInputs.forEach((input) => {
        input.classList.remove('is-valid')
        input.classList.add('is-invalid')
        inputFieldBlock = input.closest('.field-block')
        inputErrorBlock = inputFieldBlock.querySelector('.invalid-feedback')
        inputErrorBlock.innerHTML = 'Вы ничего не изменили.'
    })
}

function displayErrorEmptyField() {
    changeModalInputs.forEach((input) => {
        input.classList.remove('is-valid')
        input.classList.add('is-invalid')
        inputFieldBlock = input.closest('.field-block')
        inputErrorBlock = inputFieldBlock.querySelector('.invalid-feedback')
        inputErrorBlock.innerHTML = 'Обязательное поле.'
    })
}

function removeErrorField() {
    changeModalInputs.forEach((input) => {
        input.classList.remove('is-valid')
        input.classList.remove('is-invalid')
        inputFieldBlock = input.closest('.field-block')
        inputErrorBlock = inputFieldBlock.querySelector('.invalid-feedback')
        inputErrorBlock.innerHTML = ''
    })
}

function displaySuccessField() {
    changeModalInputs.forEach((input) => {
        input.classList.remove('is-invalid')
        input.classList.add('is-valid')
        inputFieldBlock = input.closest('.field-block')
        inputErrorBlock = inputFieldBlock.querySelector('.invalid-feedback')
        inputErrorBlock.innerHTML = ''
    })
}

function displayErrorField(error) {
    changeModalInputs.forEach((input) => {
        input.classList.remove('is-valid')
        input.classList.add('is-invalid')
        inputFieldBlock = input.closest('.field-block')
        inputErrorBlock = inputFieldBlock.querySelector('.invalid-feedback')
        inputErrorBlock.innerHTML = error
    })
}