const soldBtns = document.querySelectorAll('.sold-btn')
document.querySelector('[data-active-sold-status]').dataset.activeSoldStatus = 'all'

let soldValue = null
let userId = null

soldBtns.forEach((element) => {
    element.addEventListener('click', (e) => {
        soldValue = element.dataset.value
        userId = element.dataset.user
        if (['all', 'true', 'false'].includes(soldValue)) {
            soldBtns.forEach((el) => {
                el.classList.remove('link-primary')
                el.classList.remove('dark-link')
            })
            element.classList.remove('dark-link')
            element.classList.add('link-primary')
            sendAnnouncementsFilterRequest()
        }
    })
})