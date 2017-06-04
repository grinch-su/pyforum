$('body').show();
$('.version').text(NProgress.version);
NProgress.start();
setTimeout(function () {
    NProgress.done();
    $('.fade').removeClass('out');
}, 1000);

$("#b-0").click(function () {
    NProgress.start();
});
$("#b-40").click(function () {
    NProgress.set(0.4);
});
$("#b-inc").click(function () {
    NProgress.inc();
});
$("#b-100").click(function () {
    NProgress.done();
});

$("#alert").fadeTo(3000, 500).slideUp(500, function () {
    $("#alert").alert('close');
});

// $.get('data', function (data, status) {
//     console.log(data, status)
// });