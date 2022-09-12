const year = new Date().getFullYear().toString()

$('.main_slider').slick({
    autoplay: true,
    fade: true,
    arrows: false,
    dots: true,
});

$('.users_slider').slick({
    arrow: false,
    nextArrow: '<button class="arrow-arrow arrow-right"><img src="/static/images/arrow_right.png" alt="next slick-arrow"></button>',
    prevArrow: '<button class="arrow-arrow arrow-left"><img src="/static/images/arrow_left.png" alt="prev slick-arrow"></button>',
    slidesToShow: 4,
    responsive: [
        {
            breakpoint: 1001,
            settings: {
                slidesToShow: 3,
            }
        },
        {
            breakpoint: 751,
            settings: {
                slidesToShow: 2,
            }
        },
        {
            breakpoint: 551,
            settings: {
                slidesToShow: 1,
            }
        },
    ]
});

$(".menu_burger,.menu_close").click(function (e) {
    $(".menu_burger,.menu").toggleClass('active')
})

$(".aside_burger").click(function (e) {
    $(".aside_burger,.news_aside").toggleClass('active')
})

let select = function () {
    let selectHeader = document.querySelectorAll('.select_header');

    let selectItem = document.querySelectorAll('.select_item');
    selectHeader.forEach(item => {
        item.addEventListener('click', selectToggle)
    });

    selectItem.forEach(item => {
        item.addEventListener('click', selectChoose)
    });


    function selectToggle() {
        this.parentElement.classList.toggle('active');
    };
    function selectChoose() {
        let text = this.innerText,
            select = this.closest('.select'),
            currentText = select.querySelector('.select_current');
        currentText.innerText = text;
        select.classList.remove('active')
    }
};

$('.message_block span').click(function(){
    $('.message_block').remove();
});




select();
