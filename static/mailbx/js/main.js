$(function () {
    // 回到顶部按钮
    $('.backtop').click(function () {
        $('body,html').animate({ scrollTop: 0 })
    })

    $('.backtop').hover(function () {
        $(this).css('color', 'red')
    }, function () {
        $(this).css('color', 'black')
    })
})