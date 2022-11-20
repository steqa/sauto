const form = document.querySelector('#registration_form')

function renderReturnedData(data) {
    if (data['status'] == 400) {
        if (data['type'] == 'BadRequest') {
            return showToast(data['body']['error'], type='error')
        } else if (data['type'] == 'ValidationError') {
            if (inputType == 'submit') {
                formFields.forEach((field) => {
                    changeValidationStatusField(data, field)
                })
            } else if (inputType == 'input') {
                changeValidationStatusField(data, field = inputField)
            }
        } else if (data['type'] == 'EmailSendingError') {
            return showToast(data['body']['error'], type='error')
        }
    } else if (data['status'] == 200) {
        if (data['body']['action'] == 'ConfirmEmail') {
            document.querySelector('.content-block').innerHTML = data['body']['template']
            timerBtn(dataOutside=data)
        } else {
            formFields.forEach((field) => {
                changeValidationStatusField(data, field)
            })
        }
    }
}