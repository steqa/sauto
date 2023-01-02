function sendAnnouncementsFilterRequest() {
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