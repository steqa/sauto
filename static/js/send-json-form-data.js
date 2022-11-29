function getJsonFormData(form) {
    const elems = form.elements,
        dataArr = new Object;
    for (let i = 0; i < elems.length; i++) {
        if ((elems[i].nodeName != 'BUTTON') & (elems[i].hasAttribute('data-exclude-getFormData') === false) & (elems[i].name != '')) {
            dataArr[elems[i].name] = elems[i].value
        }
    }
    return dataArr
}

function sendJsonFormData(form, reload) {
    const formData = getJsonFormData(form)
    let url = form.action
    if (reload) {
        url += '?reload=true'
    }
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            formData,
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            renderReturnedData(data)
        })
}