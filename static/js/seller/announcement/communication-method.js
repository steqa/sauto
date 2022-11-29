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

const sellerInputs = document.querySelectorAll('.sellerFields .form-control')

sellerInputs.forEach((element) => {
    element.addEventListener('input', (e) => {
        const radioID = element.parentElement.getAttribute('data-communication-method-input-id')
        const radio = document.getElementById(radioID)
        if (element.value != '') {
            radio.disabled = false
        } else {
            radio.disabled = true
            if (radio.checked) {
                radio.checked = false
                radios[0].checked = true
                communicationMethod.value = radios[0].value
            }
        }
    })
})