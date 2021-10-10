import {redirect_to_profile} from "./user_list.js";

export function create_user_list(data, avatarHeight, parentNode, first_line = false, last_line = false){
    /*
    Each element of 'data' needs to have keys:
    'avatar_url' - contains url to user avatar,
    'display_name' - contains name to display (first line)
    'username' - contains username (second line)
    'user_pk' - id of user

    'avatarHeight needs a unit (px, %, em, etc.)
    'first_line' - enables or disables horizontal line above first element
    'last_line' - enables or disables horizontal line under last element
    */
    let container = document.createElement('div')
    container.classList.add("container")
    for(const [index, user] of Object.entries(data)){
        index == 0 && !first_line ? {} :  container.appendChild(document.createElement('hr'))// If it is first element don't draw horizontal line
        // Add clickable row that will contain avatar, display name, username and will redirect to profile page when clicked
        let clickableRow = document.createElement('div')
        clickableRow.classList.add("row", "clickable")
        // Add redirection to row
        clickableRow.onclick = () =>{
            redirect_to_profile(`/profile/${user['user_pk']}`)
        }
        // Column for avatar
        let avatarColumn = document.createElement('div')
        avatarColumn.classList.add('col-sm-2')
        let avatarPicture = document.createElement('img')
        avatarPicture.setAttribute('src', user['avatar_url'])
        avatarPicture.style.height = avatarHeight
        avatarPicture.style.borderRadius = avatarHeight
        // Append picture and column to row
        avatarColumn.appendChild(avatarPicture)
        clickableRow.appendChild(avatarColumn)
        // Create username rows
        let nameColumn = document.createElement('div')
        nameColumn.classList.add('col-sm-10')
        let displayNameRow = document.createElement('div')
        displayNameRow.classList.add('row')
        let displayName = document.createElement('a')
        displayName.style.fontWeight = 'bold'
        displayName.textContent = user['display_name']
        displayNameRow.appendChild(displayName) // Append displayName to row
        nameColumn.appendChild(displayNameRow) // Append row to column
        let usernameRow = document.createElement('div')
        usernameRow.classList.add('row')
        let username = document.createElement('a')
        username.textContent = user['username']
        usernameRow.appendChild(username) // Append username to row
        nameColumn.appendChild(usernameRow) // Append row to column
        clickableRow.appendChild(nameColumn) // Append column with names to main row

        container.appendChild(clickableRow) // Append clickableRow to container
    }
    !first_line ? {} :  container.appendChild(document.createElement('hr'))
    parentNode.appendChild(container) // Append container to parentNode
}