let data = {};
for (let i = 0; i < $('select').length; i++) {
    for (let j = 0 ; j < $('select')[i].length ; j++) {
        if ($('select')[i][j].selected) {
            data[$('select')[i].name] = $('select')[i][j].innerHTML  ;
        }
    }
}


// check if the user has already accepted the request
let accepted = false ;
$.ajax({
    type: 'GET',
    url: checkAccept,
    data: {
        'workshop' : data['workshop'] ,  
        'user' : data['user']
    },
    success: function(data) {
        if (data.message === 'Accepted') {
            accepted = true ;
        }
    },
    error: function(err) {
        console.log(err);
        alert('Error Occured');
    }
}).then (function() {
    // making the accept button
    let acceptContainer = document.createElement('form');
    acceptContainer.className = 'form-group';
    let acceptWorkshop = document.createElement('input');
    acceptWorkshop.id = 'acceptWorkshop';
    acceptWorkshop.type = 'submit';
    if (accepted) {
        acceptWorkshop.value = 'Accepted';
        acceptWorkshop.disabled = true;
    }else {
        acceptWorkshop.value = 'Accept Request';
    }
    acceptWorkshop.className = 'btn btn-success form-control';
    acceptContainer.name = "acceptWorkshop";
    acceptContainer.addEventListener('submit', function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: accept,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val() , 
                'workshop' : data['workshop'] ,  
                'user' : data['user']
            },
            success: function(data) {
                acceptWorkshop.disabled = true;
                acceptWorkshop.value = 'Accepted';
            },
            error: function(err) {
                console.log(err);
            }
        }
        )
    });
    acceptContainer.appendChild(acceptWorkshop);
    $('#jazzy-actions').children(':first').append(acceptContainer)  ;
});



$('document').ready(function() {
    $('select').prop('disabled', true)
    $('.select2-selection__arrow').remove()
});