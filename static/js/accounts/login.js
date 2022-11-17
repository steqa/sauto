const form = document.querySelector('#login_form')

function renderReturnedData(data) {
    if (data['status'] == 400) {
        if (data['type'] == 'BadRequest') {
            return showError(data['body']['error'])
        } else if (data['type'] == 'ValidationError') {
            if (inputType == 'submit') {
                formFields.forEach((field) => {
                    changeValidationStatusField(data, field)
                })
            } else if (inputType == 'input') {
                changeValidationStatusField(data, field = inputField)
            }
        } else if (data['type'] == 'AuthenticationError') {
            return showError(data['body']['error'])
        }
    } else if (data['status'] == 200) {
        if (data['type'] == 'redirect') {
            window.location.replace(data['body']['url'])
        } else {
            formFields.forEach((field) => {
                changeValidationStatusField(data, field)
            })
        }
    }
}