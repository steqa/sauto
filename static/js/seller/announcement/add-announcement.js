const form = document.querySelector('#add_announcement_form')

function renderReturnedData(data) {
    console.log(data)
    if (data['status'] == 400) {
        if (data['type'] == 'BadRequest') {
            return showToast(data['body']['error'], type = 'error')
        } else if (data['type'] == 'ValidationError') {
            if (inputType == 'input') {
                if (['id_phone_number_0', 'id_phone_number_1', 'id_telegram_username'].includes(inputField.id)) {
                    sellerDataChangeValidationStatusField(data, field = inputField)
                } else {
                    changeValidationStatusField(data, field = inputField)
                }
            }
        } else if (data['type'] == 'ImageValidationError') {

        }
    } else if (data['status'] == 200) {

    }
}