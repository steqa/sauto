const changeModal = document.querySelector('.change-modal')
const changeModalTitle = changeModal.querySelector('h1')
const changeModalInput = changeModal.querySelector('input')
const changeModalInputAsList = changeModal.querySelectorAll('input')
const changeModalInputErrorField = changeModalInput.closest('.field-block').querySelector('div.invalid-feedback')
const changeModalSubmitBtn = changeModal.querySelector('button[type="submit"]')
const form = changeModal.querySelector('form')

let inputType = null

changeModalSubmitBtn.addEventListener('click', (e) => {
    e.preventDefault()
    inputType = 'submit'
    if (checkFieldChange()) {
        sendJsonFormData(changeModalInputAsList, reload = true, action = changeModalSubmitBtn.dataset.action)
    } else {
        displayErrorUnchangedField()
    }
})

changeModalInput.addEventListener('input', (e) => {
    inputType = 'input'
    if (checkFieldChange()) {
        sendJsonFormData(changeModalInputAsList, reload = false, action = changeModalSubmitBtn.dataset.action)
    } else {
        displayErrorUnchangedField()
    }
})

const userDataChangeBtns = document.querySelectorAll('.user-data-change-btn')

userDataChangeBtns.forEach((element) => {
    element.addEventListener('click', (e) => {
        removeErrorField()
        changeModalTitle.innerHTML = element.dataset.modalTitle
        changeModalInput.type = element.dataset.modalInputType
        changeModalInput.name = element.dataset.modalInputName
        changeModalInput.value = element.dataset.modalInputValue
        changeModalSubmitBtn.dataset.action = 'change-user-data'
    })
})

function renderReturnedData(data) {
    console.log(data)
    if (data['status'] == 400) {
        if (data['type'] == 'ValidationError') {
            if (changeModalInput.name in data['body']) {
                displayErrorField()
                changeModalInputErrorField.innerHTML = data['body'][changeModalInput.type]
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

function checkFieldChange() {
    const userDataChangeBtn = document.querySelector(`[data-modal-input-name="${changeModalInput.name}"]`)
    if (userDataChangeBtn.dataset.modalInputValue != changeModalInput.value) {
        return true
    } else {
        return false
    }
}

function displayErrorUnchangedField() {
    changeModalInput.classList.remove('is-valid')
    changeModalInput.classList.add('is-invalid')
    changeModalInputErrorField.innerHTML = 'Вы ничего не изменили.'
}

function removeErrorField() {
    changeModalInput.classList.remove('is-valid')
    changeModalInput.classList.remove('is-invalid')
    changeModalInputErrorField.innerHTML = ''
}

function displaySuccessField() {
    changeModalInput.classList.remove('is-invalid')
    changeModalInput.classList.add('is-valid')
    changeModalInputErrorField.innerHTML = ''
}

function displayErrorField() {
    changeModalInput.classList.remove('is-valid')
    changeModalInput.classList.add('is-invalid')
    changeModalInputErrorField.innerHTML = ''
}