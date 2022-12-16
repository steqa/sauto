if (document.querySelectorAll('.swiper-slide').length > 1) {
    loop = true
} else {
    loop = false
}
const swiper = new Swiper('.swiper', {
    loop: loop,
    zoom: true,
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
})