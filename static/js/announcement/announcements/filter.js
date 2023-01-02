const filterFieldsNumber = document.querySelectorAll('input[type="number"]')
const filterFieldsCheckbox = document.querySelectorAll('input[type="checkbox"]')
const filterFieldsRadio = document.querySelectorAll('input[type="radio"]')
let filterValues = new Map()

filterFieldsNumber.forEach((field) => {
    let time
    field.addEventListener('input', (e) => {
        clearTimeout(time)
        time = setTimeout((e) => {
            const fieldType = field.dataset.filterFieldType
            const fieldValue = field.value
            if (fieldValue != '') {
                filterValues.set(fieldType, fieldValue)
            } else {
                filterValues.delete(fieldType)
            }
            sendAnnouncementsFilterRequest()
        }, 300)
    })
})

filterFieldsCheckbox.forEach((field) => {
    field.addEventListener('input', (e) => {
        const fieldType = field.dataset.filterFieldType
        const fieldValue = field.value
        if (field.checked) {
            if (filterValues.get(fieldType)) {
                filterValues.get(fieldType).push(fieldValue)
            } else {
                filterValues.set(fieldType, [fieldValue])
            }
        } else {
            const fieldIndex = filterValues.get(fieldType).indexOf(fieldValue)
            filterValues.get(fieldType).splice(fieldIndex, 1)
            if (filterValues.get(fieldType) == '') {
                filterValues.delete(fieldType)
            }
        }
        sendAnnouncementsFilterRequest()
    })
})

filterFieldsRadio.forEach((field) => {
    field.addEventListener('input', (e) => {
        const fieldType = field.dataset.filterFieldType
        const fieldValue = field.value
        filterValues.set(fieldType, fieldValue)
        sendAnnouncementsFilterRequest()
    })
})