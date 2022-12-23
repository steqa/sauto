function formUrl() {
    let url = window.location.href
    if (window.location.href.split('?').length == 1) {
        url += '?'
    } else {
        url += '&'
    }
    if (filterValues.size > 0) {
        url += 'filter=true&'
        let urlParams = ''
        filterValues.forEach((value, key) => {
            urlParams += `${key}=${value}&`
        })
        url += urlParams
    }
    if (searchField.value != '') {
        url += `search=${searchField.value}&`
    }
    if ((filterValues.size <= 0) & (searchField.value == '')) {
        url += 'all=true'
    }
    return url
}