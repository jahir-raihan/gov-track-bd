$(document).on('submit', '#upload-file', function(e){
    e.preventDefault();
    var data = new FormData($('#upload-file').get(0));
    e.preventDefault();
    let req = $.ajax({
        type: 'post',
        url : '/upload-file/',
        data: data,
        cache: false,
        processData: false,
        contentType: false


    })
    req.done(function(data){
        console.log(data)
        $('#card').html(data)

    })
})