const formFields = document.querySelectorAll('.form-control')

let inputType = null
let inputField = null

form.addEventListener('submit', function (e) {
    e.preventDefault()
    inputType = 'submit'
    sendJsonFormData(this, reload = true)
})

formFields.forEach((element) => {
    element.addEventListener('input', function (e) {
        inputType = 'input'
        inputField = element
        sendJsonFormData(form, reload = false)
    })
})