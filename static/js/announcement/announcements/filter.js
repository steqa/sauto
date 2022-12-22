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
            sendFilteringRequest()
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
        sendFilteringRequest()
    })
})

filterFieldsRadio.forEach((field) => {
    field.addEventListener('input', (e) => {
        const fieldType = field.dataset.filterFieldType
        const fieldValue = field.value
        filterValues.set(fieldType, fieldValue)
        sendFilteringRequest()
    })
})

function sendFilteringRequest() {
    const url = formUrl()
    fetch(url)

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            if (data['status'] == 400) {
                return showToast(data['body']['error'], type = 'error')
            } else if (data['status'] == 200) {
                document.querySelector('.announcement-cards').innerHTML = data['body']['template']
            }
        })
}

function formUrl() {
    let urlParams = ''
    filterValues.forEach((value, key) => {
        urlParams += `${key}=${value}&`
    })
    return window.location.href + '?filter=true&' + urlParams
}