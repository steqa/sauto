changeSoldStatusBtns = document.querySelectorAll('.change-sold-status-btn')

changeSoldStatusBtns.forEach((element) => {
    element.addEventListener('click', (e) => {
        sendChangeSoldStatusRequest(element)
    })
})

function sendChangeSoldStatusRequest(element) {
    fetch(element.dataset.href)

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            if (data['status'] == 400) {
                return showToast(data['body']['error'], type = 'error')
            } else if (data['status'] == 200) {
                const dropdownMenu = element.closest('.dropdown-menu')
                const card = element.closest('.col')
                if (document.querySelector('[data-active-sold-status]').dataset.activeSoldStatus == 'all') {
                    const soldStatusFlag = card.querySelector('.sold-status')
                    if (element.dataset.status == 'sold') {
                        soldStatusFlag.classList.remove('sold-status-false')
                        soldStatusFlag.classList.add('sold-status-true')
                        soldStatusFlag.innerHTML = 'Продано'
                        dropdownMenu.querySelector('[data-sold-status="sold"]').style.display = 'none'
                        dropdownMenu.querySelector('[data-sold-status="not-sold"]').style.display = 'flex'
                    } else if (element.dataset.status == 'not-sold') {
                        soldStatusFlag.classList.remove('sold-status-true')
                        soldStatusFlag.classList.add('sold-status-false')
                        soldStatusFlag.innerHTML = 'Не продано'
                        dropdownMenu.querySelector('[data-sold-status="sold"]').style.display = 'flex'
                        dropdownMenu.querySelector('[data-sold-status="not-sold"]').style.display = 'none'
                    }
                } else { 
                    card.remove()
                }
                return showToast(data['body']['success'], type = 'success')
            }
        })
}