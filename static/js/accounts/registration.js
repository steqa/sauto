const form = document.querySelector('#registration_form')

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
        } else if (data['type'] == 'EmailSendingError') {
            return showError(data['body']['error'])
        }
    } else if (data['status'] == 200) {
        if (data['body']['action'] == 'confirm_email') {
            document.querySelector('.content-block').innerHTML = data['body']['template']
        } else {
            formFields.forEach((field) => {
                changeValidationStatusField(data, field)
            })
        }
    }
}