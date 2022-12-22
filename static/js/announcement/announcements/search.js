const searchField = document.querySelector('input[type="search"]')

let time
searchField.addEventListener('input', (e) => {
    clearTimeout(time)
    time = setTimeout((e) => {
        sendFilteringRequest()
    }, 800)
})