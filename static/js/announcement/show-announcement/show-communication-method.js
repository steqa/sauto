const showContactInfoBtn = document.getElementById('show-contact-info')

showContactInfoBtn.addEventListener('click', (e) => {
    sendRequestContactInfo(showContactInfoBtn)
})

function sendRequestContactInfo(element) {
    fetch(`${element.dataset.action}?show-contact-info=true`)

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log(data)
            if (data['status'] == 200) {
                if (data['body']['contact_type'] == 'email') {
                    showContactInfoBtn.innerHTML = `Адрес электронной почты:<br>${data['body']['contact_info']}`
                } else if (data['body']['contact_type'] == 'telegram_username') {
                    showContactInfoBtn.innerHTML = `Имя пользователя телеграм:<br>@${data['body']['contact_info']}`
                } else if (data['body']['contact_type'] == 'phone_number') {
                    showContactInfoBtn.innerHTML = `Номер телефона:<br>${data['body']['contact_info']}`
                }
                showContactInfoBtn.classList.remove('btn-primary')
                showContactInfoBtn.classList.add('btn-outline-primary')
                showContactInfoBtn.disabled = true
            }
        })
}