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
                const deleteAnnouncementScript = document.querySelector('.delete-announcement-script')
                const changeSoldStatusAnnouncementScript = document.querySelector('.change-sold-status-announcement-script')
                const deleteAnnouncementScriptSrc = deleteAnnouncementScript.src
                const changeSoldStatusAnnouncementScriptSrc = changeSoldStatusAnnouncementScript.src
                deleteAnnouncementScript.remove()
                changeSoldStatusAnnouncementScript.remove()
                reloadScripts(deleteAnnouncementScriptSrc)
                reloadScripts(changeSoldStatusAnnouncementScriptSrc)
                if (typeof soldValue !== "undefined") {
                    document.querySelector('[data-active-sold-status]').dataset.activeSoldStatus = soldValue
                }
            }
        })
}

function reloadScripts(url) {
    const script = document.createElement('script')
    script.type = 'text/javascript'
    script.src = url
    document.documentElement.appendChild(script)
}