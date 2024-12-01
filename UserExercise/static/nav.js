                                
const swiper = new Swiper(".featured-slider", {
    spaceBetween: 30,
    loop:true,
    centeredSlides:true, 
    autoplay: {
        delay: 6500,
        disableOnInteraction: false,
    },
    navigation:{
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        450: {
            slidesPerView: 2,
        },
        768: {
            slidesPerView: 3,
        },
        1024: {
            slidesPerView: 4,
        },
    },
});

window.onscroll = () => {
            const nav = document.querySelector('.navbar');
            if(this.scrollY <= 230) nav.className = 'navbar'; else nav.className = 'navbar scroll';
        };       