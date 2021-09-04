function change_button_follow(btn_id){
    var btn = document.getElementById(btn_id);
    var icon = document.querySelector('#' + btn_id + ' img');
    var follow_text = document.querySelector('#' + btn_id + ' a');
    icon.src = "/static/icons/person-check-fill.svg";
    btn.classList.add("follow-btn-followed");
    btn.classList.remove("follow-btn-unfollowed");
    follow_text.innerHTML = "Followed";
}

function change_button_unfollow(btn_id){
    var btn = document.getElementById(btn_id);
    var icon = document.querySelector('#' + btn_id + ' img');
    var follow_text = document.querySelector('#' + btn_id + ' a');
    icon.src = "/static/icons/person-plus-fill.svg";
    btn.classList.add("follow-btn-unfollowed");
    btn.classList.remove("follow-btn-followed");
    follow_text.innerHTML = "Follow";
}

//This function will be universal so url for follow view must be passes as argument
function follow(follow_url, button_id){
    follow_url = window.location.pathname + follow_url;
    $.ajax({
        type: 'GET',
        url: follow_url,
        success: function (response){
            var like_status = response['follow_status'];
            like_status ? change_button_follow(button_id) : change_button_unfollow(button_id);

        },
        error: function(response){
            alert(response['message']);
        }
    })
}


