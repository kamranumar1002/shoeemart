var isotopeButton = $('.filter-tope-group button');

$(isotopeButton).each(function(){
    $(this).on('click', function(){
        for(var i=0; i<isotopeButton.length; i++) {
            $(isotopeButton[i]).removeClass('how-active1');
        }

        $(this).addClass('how-active1');
    });
});

$('.js-show-search').on('click',function(){
    $(this).toggleClass('show-search');
    $('.panel-search').slideToggle(400);

    if($('.js-show-filter').hasClass('show-filter')) {
        $('.js-show-filter').removeClass('show-filter');
        $('.panel-filter').slideUp(400);
    }    
});