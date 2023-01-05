function renderReturnedData(data) {
    if (data['status'] == 400) {
        if (data['type'] == 'BadRequest') {
            return showToast(data['body']['error'], type = 'error')
        }
        if (data['type'] == 'ValidationError') {
            if (inputType == 'input') {
                if (['id_phone_number_0', 'id_phone_number_1', 'id_telegram_username'].includes(inputField.id)) {
                    sellerChangeValidationStatusField(data, field = inputField)
                } else if (inputField == 'location') {
                    locationChangeValidationStatusField(data)
                } else if (inputField == 'communicationMethod') {

                } else {
                    changeValidationStatusField(data, field = inputField)
                }
            } else if (inputType == 'submit') {
                changeValidationStatusAllFields(data)
            }
        }
        if (data['type'] == 'ImageValidationError') {
            imageFields.forEach((field) => {
                imageChangeValidationStatusField(data, field = field)
            })
        }
    } else if (data['status'] == 200) {
        if (data['type'] == 'redirect') {
            localStorage.setItem('status', data['status'])
            localStorage.setItem('message', data['body']['success'])
            console.log(data['body']['url'])
            window.location.replace(data['body']['url'])
        } else {
            changeValidationStatusAllFields(data)
        }
    }
}

function changeValidationStatusAllFields(data) {
    announcementFields.forEach((field) => {
        changeValidationStatusField(data, field = field)
    })
    locationChangeValidationStatusField(data)
    imageFields.forEach((field) => {
        imageChangeValidationStatusField(data, field = field)
    })
    sellerFields.forEach((field) => {
        sellerChangeValidationStatusField(data, field = field)
    })
}