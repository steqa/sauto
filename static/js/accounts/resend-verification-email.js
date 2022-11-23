const RESEND_TIMEOUT = 300


function timerBtn(dataOutside) {
    const now = new Date()
    const deadline = now.setSeconds(now.getSeconds() + RESEND_TIMEOUT)
    const resendBtn = document.getElementById('resendBtn')
    let timerId = null

    const timeCount = () => {
        if (resendBtn.hasAttribute('disabled') === false) {
            resendBtn.setAttribute('disabled', 'true')
        }

        const now = new Date()
        const leftUntilSend = deadline - now

        const minutes = (Math.floor(leftUntilSend / 1000 / 60) % 60).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false })
        const seconds = (Math.floor(leftUntilSend / 1000) % 60).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false })

        resendBtn.innerHTML = `Отправить повторно через ${minutes}:${seconds}`

        if (leftUntilSend <= 0) {
            clearInterval(timerId)
            activateResendBtn(dataOutside)
        }
    }

    timeCount()
    timerId = setInterval(timeCount, 1000)
}

function activateResendBtn(dataOutside) {
    const resendBtn = document.getElementById('resendBtn')
    resendBtn.innerHTML = 'Отправить повторно'
    resendBtn.removeAttribute('disabled')

    resendBtn.addEventListener('click', () => {
        resendBtn.setAttribute('disabled', 'true')
        sendEmail(dataOutside)
    }, {once: true})
}

function sendEmail(dataOutside) {
    const url = `/account/resend-verification-email/${dataOutside['body']['uidb64']}`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            const resendBtn = document.getElementById('resendBtn')
            if (data['status'] == 200) {
                resendBtn.innerHTML = 'Отправленно'
                document.getElementById('resendSuccessHint').classList.remove('visually-hidden')
                showToast(data['body']['success'], type = 'success')
            } else if (data['status'] == 400) {
                resendBtn.innerHTML = 'Не отправленно'
                document.getElementById('resendErrorHint').classList.remove('visually-hidden')
                showToast(data['body']['error'], type = 'error')
            }
        })
}