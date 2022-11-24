function showToast(msg, type) {
    const toast = document.getElementById('toast')
    const message = toast.querySelector('.toast-body')
    if (type == 'error') {
        toast.classList.remove('text-bg-success')
        toast.classList.add('text-bg-danger')
    } else if (type == 'success') {
        toast.classList.remove('text-bg-danger')
        toast.classList.add('text-bg-success')
    }
    message.innerHTML = msg
    const toastShow = new bootstrap.Toast(toast)
    toastShow.show()
}

if (localStorage.getItem('status')) {
    msg = localStorage.getItem('message')
    if (localStorage.getItem('status') == 400) {
        type = 'error'
    } else if (localStorage.getItem('status') == 200) {
        type = 'success'
    }
    showToast(msg, type)
    localStorage.clear();
}