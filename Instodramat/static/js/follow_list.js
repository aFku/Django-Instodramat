const body = document.body

function generate_content(response){
    content = response['data'];
    meta = response['meta']
    var modalString = body.innerHTML + `
        <div class="modal" tabindex="-1" id="modal-content" style="display: block;">
            <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${meta['title']}</h5>
                    </div>
                     <div class="modal-body">
`;
      modalString += `<div class="container"> `;
      for(index in content){
      index == 0 ? modalString += '' : modalString += '<hr>' ;
      modalString += `<div class="row" onclick="redirect_to_profile('/profile/${content[index]['user_pk']}')"> `;
      modalString += `<div class="col-sm-2">`;
      modalString += `<img src=${content[index]['avatar_url']} style="height: 50px; border-radius: 50px;">`;
      modalString += `</div>`;
      modalString += `<div class="col-sm-10">`;
      modalString += `<div class="row">`;
      modalString += `<a style="font-weight: bold;">${content[index]['first_name']} ${content[index]['last_name']}</a><br>`;
      modalString += `</div>`;
      modalString += `<div class="row">`;
      modalString += `<a>${content[index]['username']}</a>`;
      modalString += `</div>`;
      modalString += `</div>`;

      modalString += `</div> `;
      }
      modalString += `</div> `;
      modalString += `
                     </div>
                     <div class="modal-footer">
                        <button type="button" class="btn btn-primary" id="crop-button">Save</button>
                    </div>
                </div>
            </div>
        </div>
`;
    body.innerHTML = body.innerHTML + modalString;
}


function get_list(view_url){
    $.ajax({
        type: 'GET',
        url: view_url,
        success: function(response){
            generate_content(response);
        },
        error: function(response){
            alert('Something went wrong.');
        }
    })
}

function redirect_to_profile(profile_url){
    window.location.href = profile_url;
}