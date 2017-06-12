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
// поиск пользователей
$('#search_user').keyup(function () {
    $('#result').html('');
    var searchField = $('#search_user').val();
    var myExp = new RegExp(searchField, 'i');
    $.getJSON('search_user', function (data) {
        $.each(data.users, function (key, val) {
            if (val.username.search(myExp) !== -1) {
                $('#result').append('<a href="'+val._link+'"><li class="list-group-item link-class" id="'+key+'">' +
                    '<img src="'+val.avatar+'" height="40" width="40" class="img-circle" />' +
                    ' '+val.username+' </li></a>');
            }
        })
    })
});