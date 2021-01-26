const icon = document.getElementById('like-icon')

function change_icon_dislike(){
    icon.src = "/static/icons/heart-thin-empty.svg";
}

function change_icon_like(){
    icon.src = "/static/icons/heart-thin-red.svg";
}


icon.addEventListener('click', ()=>{
    $.ajax({
        type: 'GET',
        url: "like",
        success: function (response){
            var like_status = response['like_status'];
            like_status ? change_icon_like() : change_icon_dislike();

        },
        error: function(response){
            alert(response['message']);
        }
    })
}

)