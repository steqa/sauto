const favoriteBtns = document.querySelectorAll('[data-favorite-btn')

favoriteBtns.forEach((element) => {
    element.addEventListener('click', (e) => {
        sendData(element)
    })
})

function sendData(element) {
    fetch(element.dataset.action)

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            if (data['status'] == 400) {
                if ((data['type'] == 'BadRequest') || (data['type'] == 'AuthenticationError')) {
                    return showToast(data['body']['error'], type = 'error')
                } else if (data['type'] == 'ValidationError') {
                    changeFavoriteBtn(element)
                    return showToast(data['body']['error'], type = 'error')
                }
            } else if (data['status'] == 200) {
                changeFavoriteBtn(element)
            }
        })
}

function changeFavoriteBtn(element) {
    if (element.dataset.favoriteBtnType == 'add') {
        element.style.display = 'none'
        const removeFavoriteBtn = document.querySelector(`[data-favorite-btn="${element.dataset.favoriteBtn}"][data-favorite-btn-type="remove"]`)
        removeFavoriteBtn.style.display = 'block'
    } else if (element.dataset.favoriteBtnType == 'remove') {
        element.style.display = 'none'
        const addFavoriteBtn = document.querySelector(`[data-favorite-btn="${element.dataset.favoriteBtn}"][data-favorite-btn-type="add"]`)
        addFavoriteBtn.style.display = 'block'
    }
}