function changeValidationStatusField(data, field) {
    if (field) {
        const invalidFeedbackBlock = field.closest('.field-block').querySelector('.invalid-feedback')
        const fieldName = field.getAttribute('name')
        if (fieldName in data['body']) {
            field.classList.remove('is-valid')
            field.classList.add('is-invalid')
            invalidFeedbackBlock.innerHTML = data['body'][fieldName].join("<br>")
        } else {
            field.classList.remove('is-invalid')
            field.classList.add('is-valid')
            invalidFeedbackBlock.innerHTML = ''
        }
    }
}