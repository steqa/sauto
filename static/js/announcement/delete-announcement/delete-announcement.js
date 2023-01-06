const deleteAnnouncementBtns = document.querySelectorAll('.delete-announcement-btn')
const deleteModal = document.querySelector('.modal')
const modalDeleteBtn = deleteModal.querySelector('button[type="submit"]')

deleteAnnouncementBtns.forEach((element) => {
    element.addEventListener('click', (e) => {
        modalDeleteBtn.dataset.href = element.dataset.href
        modalDeleteBtn.dataset.deleteAnnouncement = element.dataset.announcementDelete
    })
})

modalDeleteBtn.addEventListener('click', (ev) => {
    const deleteAnnouncement = document.querySelector(`[data-announcement="${modalDeleteBtn.dataset.deleteAnnouncement}"]`)
    sendDeleteRequest(deleteAnnouncement, modalDeleteBtn)
})

function sendDeleteRequest(deleteAnnouncement, modalDeleteBtn) {
    fetch(modalDeleteBtn.dataset.href)

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            if (data['status'] == 400) {
                return showToast(data['body']['error'], type = 'error')
            } else if (data['status'] == 200) {
                deleteAnnouncement.closest('div.col').remove()
                return showToast(data['body']['success'], type = 'success')
            }
        })
}