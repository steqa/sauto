function formUrl() {
    let url = window.location.href
    let all = true
    if (window.location.href.split('?').length == 1) {
        url += '?'
    } else {
        url += '&'
    }
    if (typeof filterValues !== 'undefined') {
        if (filterValues.size > 0) {
            all = false
            url += 'filter=true&'
            let urlParams = ''
            filterValues.forEach((value, key) => {
                urlParams += `${key}=${value}&`
            })
            url += urlParams
        }
    }
    if (typeof searchField !== 'undefined') {
        if (searchField.value != '') {
            all = false
            url += `search=${searchField.value}&`
        }
    }
    if (typeof soldValue !== 'undefined') {
        if (soldValue != null){
            all = false
            url += `filter_by_seller_and_sold=true&sold=${soldValue}&user_pk=${userId}&`
        }
    }
    if (all) {
        url += 'all=true'
    }
    return url
}