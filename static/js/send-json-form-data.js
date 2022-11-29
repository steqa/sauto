function getJsonFormData(inputs) {
    const dataArr = new Object;
    for (let i = 0; i < inputs.length; i++) {
        if ((inputs[i].nodeName != 'BUTTON') & (inputs[i].name != '')) {
            dataArr[inputs[i].name] = inputs[i].value
        }
    }
    return dataArr
}

function sendJsonFormData(inputs, reload, action = null) {
    const formData = getJsonFormData(inputs)
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
            'formData': formData,
            'action': action,
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            renderReturnedData(data)
        })
}