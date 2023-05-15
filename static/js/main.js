
// function to toggle dashboard icon

function show_dash_options(){
    let ele = document.getElementById('dashboard-toggle');
    ele.classList.toggle('d-none')


    let dash = document.getElementById('dashboard-link')
    dash.classList.toggle('bg-black')


}


//  Function to filter data from User Perspective
function filter_data(){
    req = $.ajax({
        type:'POST',
        url:'/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            category:$('#category').val(),
            start_date:$('#time-range-start').val(),
            end_date:$('#time-range-end').val()
        }
    });
    req.done(function(data){
        obj = '<select name="project" required id="id_project" class="category"><option value>-------------</option>'
        for (d of data.details){
            obj += `<option value="${d[1]}"> ${d[0]} </option>`
        }
        obj += '</select>'
        $('#s-proj').html(obj)
    })
}

// Ajax part when we choose a project, this will send a request to the backend and will get a signal with information.

$(document).on('submit', '#get-project-details', function(e){

        e.preventDefault();
        document.getElementById('d-f-c-txt').classList.add('d-none')
        document.getElementById('loader').classList.remove('d-none')


        let req = $.ajax({
            type:'post',
            url: 'get-details/',
            data: {
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                project_id : $('#id_project').val()

            }


        });
        req.done(function(data){
            document.getElementById('loader').classList.add('d-none')
            document.getElementById('detail-box').classList.remove('d-none')
            document.getElementById('d-f-c-txt').classList.add('d-none')
            var p = data.project
            $('#project-name').html(p[0]); $('#affiliated-agency').html(p[1]);
            $('#description').html(p[2]); $('#start-time').html(p[3]); $('#completion-time').html(p[4]);
            $('#total-budget').html(p[5]); $('#completion-percentage').html(p[6]);
            $('#time-remaining-percentage').html(p[8])
            $('#section-map').html('<div id="empty"></div>');
            document.getElementById('issue-hidden-val').setAttribute('value', p[0])
            document.getElementById('issue-hidden-id').setAttribute('value', p[7])
            $('#b-csrf').before(`<input type="hidden" name="csrfmiddlewaretoken" value='${data.csrf}'> `)

            var cor = data.coordinates
            i = 1
            for (c of cor){
                if (data.l_c > 1){
                    cnt = `<p>Location on map (${i})</p>`
                    i += 1
                }
                else{
                    cnt = '<p> Location on map</p>'
                }
                tmp = `<div class="map-title">
                            ${cnt}
                            <iframe class="map" loading="lazy" allowfullscreen src="https://www.google.com/maps/embed/v1/place?q=${c[0]}%2C%20${c[1]}&key=AIzaSyB8o0153cfwDCEF5s5GwjareVZb5p-5zLk"></iframe>
                       </div>`
                $('#empty').before(tmp)

            }
        });




});

function rate(val){

    document.getElementById('rating').setAttribute('value', val)
}




// Admin page Ajax , For Admin's to filter and sort by project names or Issue counts on them.


$(document).on('submit', '#filter-by-admin-page', function(e){
    $('#detail').html('<div id="empty-a-det"></div>')
    e.preventDefault()
    let req = $.ajax({
        type:'post',
        url: '/admin-page/',
        data: {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            keyword : $('#keyword').val(),
            sort: $('#sort-issue:checked').val()

        }
    });
    req.done(function(data){
        document.getElementById('d-f-c-txt').classList.add('d-none')
        document.getElementById('detail-box').classList.remove('d-none')
        var i = 1;
        for (d of data.projects){
            obj = `<p class="d-l" p_id="${d[1]}">${i})  Issues<b>(${d[2]})</b> -->  ${d[0]}</p>`
            $('#empty-a-det').before(obj)
            i += 1
        }

    })
})

// For visualizing the Geo Data

$(document).on('click', '.d-l', function(e){
    var val = $(this).attr('p_id')
    $('#section-map').html('<div id="empty"></div>')

    let req = $.ajax({
        type:'post',
        url: '/get-admin-vizes/',
        data: {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            id : val

        }
    })
    req.done(function(data){
        var cor = data.coordinates
        i = 1
        for (c of cor){
            if (data.l_c > 1){
                cnt = `<p>Location on map (${i})</p>`
                i += 1
            }
            else{
                cnt = '<p> Location on map</p>'
            }
            tmp = `<div class="map-title">
                        ${cnt}
                        <iframe class="map" loading="lazy" allowfullscreen src="https://www.google.com/maps/embed/v1/place?q=${c[0]}%2C%20${c[1]}&key=AIzaSyB8o0153cfwDCEF5s5GwjareVZb5p-5zLk"></iframe>
                   </div>`
            $('#empty').before(tmp)

        }

    })

})

// Overlay Functions

function on() {
  document.getElementById("home-overlay").style.display = "block";
  document.getElementById('issue-proj-title').innerHTML = $('#issue-hidden-val').val();

}

function off() {
  document.getElementById("home-overlay").style.display = "none";

}

// Overlay issue form
$(document).on('submit', '#issue-form', function(e){
    e.preventDefault();

    let req = $.ajax({

        type:'post',
        url:'/issue-form/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            issue : $('#id_issue').val(),
            id: $('#issue-hidden-id').val(),
            rate: $('#rating').val(),
        }
    })
    req.done(function(data){
        $('#overlay-form').html('<div class="cross" onclick="off()">X</div><p style="text-align:center;"> Committed Feedback Successfully.</p>')
    })

})

// proposal acceptance

$(document).on('submit', '#accept-prop', function(e){
    e.preventDefault();
    let req = $.ajax({
        type:'post',
        url:'/m-o-p/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            id: $('#prop_id').val(),
            approval:'accept',
            date:$('#date').val()
        }

    })
    req.done(function(data){
        $(`#proposal-list${data.id}`).html(data.template)


    })

})

$(document).on('submit', '#dec-prop', function(e){
    e.preventDefault();
    let req = $.ajax({
        type:'post',
        url:'/m-o-p/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            id: $('#prop_id').val(),
            approval:'decline'
        }

    })
    req.done(function(data){
        $(`#proposal-list${data.id}`).html(data.template)


    })

})


