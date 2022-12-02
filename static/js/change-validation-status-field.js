function changeValidationStatusField(data, field) {
    if (field) {
        const invalidFeedbackBlock = field.closest('.field-block').querySelector('.invalid-feedback')
        if (field.value != '') {
            if (field.name in data['body']) {
                field.classList.remove('is-valid')
                field.classList.add('is-invalid')
                invalidFeedbackBlock.innerHTML = data['body'][field.name].join("<br>")
            } else {
                field.classList.remove('is-invalid')
                field.classList.add('is-valid')
                invalidFeedbackBlock.innerHTML = ''
            }
        } else {
            field.classList.remove('is-valid')
            field.classList.remove('is-invalid')
            invalidFeedbackBlock.innerHTML = ''
        }
    }
}