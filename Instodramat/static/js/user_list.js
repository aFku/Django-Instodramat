import {create_user_list} from "./create_user_list.js";

const body = document.body


function create_modal(parentNode, headerText, data){
    //Create main modal box
    let modal = document.createElement("div")
    modal.classList.add('modal')
    modal.setAttribute('tabindex', '-1')
    modal.id = 'modal-follow-content'
    modal.style.display = 'block'
    //Create content boxes for modal
    let modalDialog = document.createElement('div')
    modalDialog.classList.add("modal-dialog",
        "modal-dialog-centered",
        "modal-dialog-scrollable",
        "modal-lg")
    let modalContent = document.createElement('div')
    modalContent.classList.add("modal-content")
    //Create Header for modal
    let modalHeader = document.createElement('div')
    modalHeader.classList.add("modal-header")
    let headerContent = document.createElement("h5")
    headerContent.classList.add("modal-title")
    headerContent.textContent = headerText
    modalHeader.appendChild(headerContent) //Append h5 to header section
    modalContent.appendChild(modalHeader) // Append header section to modal
    //Create modal body
    let modalBody = document.createElement("div")
    modalBody.classList.add("modal-body")
    create_user_list(data, '50px', modalBody)
    modalContent.appendChild(modalBody) // Append body section to modal
    //Create modal footer
    let modalFooter = document.createElement('div')
    modalFooter.classList.add('modal-footer')
    let closeButton = document.createElement('button')
    closeButton.classList.add("btn", "btn-primary")
    closeButton.setAttribute('type', 'button')
    closeButton.textContent = 'Close'
    closeButton.onclick = () => {
        close_modal()
    }
    modalFooter.appendChild(closeButton) // Append button to modal footer
    modalContent.appendChild(modalFooter) // Append footer to modal
    modalDialog.appendChild(modalContent) // Append content to dialog
    modal.appendChild(modalDialog) // Append dialog to main modal box
    parentNode.appendChild(modal) // Append modal to parent
}

function generate_content(response){
    const data = response['data']
    const title = response['meta']['title']
    create_modal(body, title, data)
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

export function redirect_to_profile(profile_url){
    window.location.href = profile_url;
}

function close_modal(){
    var modal = document.getElementById('modal-follow-content');
    modal.remove();
}

window.get_list = get_list
window.redirect_to_profile = redirect_to_profile
window.close_modal = close_modal