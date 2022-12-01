const form = document.querySelector('#add_announcement_form')

function renderReturnedData(data) {
    console.log(data)
    if (data['status'] == 400) {
        if (data['type'] == 'BadRequest') {
            return showToast(data['body']['error'], type = 'error')
        } else if (data['type'] == 'ValidationError') {
            if (inputType == 'input') {
                changeValidationStatusField(data, field = inputField)
            }
        } else if (data['type'] == 'ImageValidationError') {

        }
    } else if (data['status'] == 200) {

    }
}