$(document).on('submit', '#register-other-user-form', function(e){

    e.preventDefault();
    var data = new FormData($('#register-other-user-form').get(0));
    let req = $.ajax({

        type:'post',
        url: '/user/register-other-users/',
        data: data,
        cache: false,
        processData: false,
        contentType: false
    });
    req.done(function(e){
        $('#s-c-register-other-roles').html(e)
    })
})

function refresh(){
    template = ` <div class="s-f-header" style="text-align:center; font-size: 20px; padding:0px 0px 10px 0px;">Register new Admin & other Roles</div><form method="post" id="register-other-user-form">
                      <label for="Name" style="opacity:.7">Name</label>
                      <input type="text" name="name" id="Name" class="category">
                      <label for="email" style="opacity:.7">Email</label>
                      <input type="email" name="email" id="email" class="category">
                      <label for="password" style="opacity:.7">Password</label>
                      <input type="password" name="password1" id="password" class="category">
                      <label for="confirmpassword" style="opacity:.7">Confirm Password</label>
                      <input type="password" name="password2" id="confirmpassword" class="category">


                      <button class="btn" type="submit">Register</button>
                  </form>`


    $('#s-c-register-other-roles').html(template)


}