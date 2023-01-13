const enableTelegramNotificationsBtn = document.querySelector('.enable-telegram-notifications-btn')
const disableTelegramNotificationsBtn = document.querySelector('.disable-telegram-notifications-btn')

if (!(typeof enableTelegramNotificationsBtn === 'undefined') & !(enableTelegramNotificationsBtn === null)) {
    enableTelegramNotificationsBtn.addEventListener('click', (e) => {
        sendTelegramNotificationData(e.target)
    })
}

if (!(typeof disableTelegramNotificationsBtn === 'undefined') & !(disableTelegramNotificationsBtn === null)) {
    disableTelegramNotificationsBtn.addEventListener('click', (e) => {
        sendTelegramNotificationData(e.target)
    })
}

function sendTelegramNotificationData(element) {
    fetch(element.dataset.action)

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            if (data['status'] == 400) {
                localStorage.setItem('status', data['status'])
                localStorage.setItem('message', data['body']['error'])
                window.location.replace(window.location.href)
            } else if (data['status'] == 200) {
                localStorage.setItem('status', data['status'])
                localStorage.setItem('message', data['body']['success'])
                window.location.replace(window.location.href)
            }
        })
}