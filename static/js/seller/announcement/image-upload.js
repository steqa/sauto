const dropArea = document.querySelectorAll('#upload-container')
const fileInputs = document.querySelectorAll('#file-input')

dropArea.forEach((elem) => {
    elem.addEventListener('dragover', function (e) {
        e.preventDefault();
    })
    elem.addEventListener('drop', function (e) {
        e.preventDefault();
        const inputName = elem.querySelector('#file-input').getAttribute('name')
        console.log(e)
        file = e.dataTransfer.files
        form.querySelector(`[name="${inputName}"]`).files = file
        files = [...file]
        files.forEach((f) => previewFile(f, elem))
        sendFormData(form, reload = false)
    })
})

fileInputs.forEach((elem) => {
    elem.addEventListener('input', function (e) {
        file = elem.files
        files = [...file]
        files.forEach((f) => previewFile(f, elem.parentNode))
        sendFormData(form, reload = false)
    })
})

function previewFile(file, elem) {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onloadend = function () {
        const img = document.createElement('img')
        img.src = reader.result
        elem.setAttribute('style', `background-image: url(${img.src}); background-repeat: no-repeat; background-position: center; background-size: cover;`)
    }
    const input = elem.querySelector('input')
    const label = elem.querySelector('label')
    const span = elem.querySelector('span')
    const button = elem.querySelector('button')
    label.setAttribute('style', 'display: none')
    span.setAttribute('style', 'display: none')
    button.setAttribute('style', 'display: block')
    button.addEventListener('click', () => {
        input.value = ''
        button.setAttribute('style', 'display: none')
        elem.removeAttribute('style')
        label.removeAttribute('style')
        span.removeAttribute('style')
        sendFormData(form, reload = false)
    })
}
