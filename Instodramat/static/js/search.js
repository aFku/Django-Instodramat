import {create_user_list} from "./create_user_list.js";

const searchbar = document.querySelector("#searchbar")

searchbar.addEventListener('input', () => {
    $.ajax({
        type: 'GET',
        url: '/community/searchajax',
        data: {
            'searchinput': searchbar.value
        },
        success: function (response) {
            setSearchResult(response)
        }
    })
})

const searchBox = document.querySelector("#search-box")


const setSearchResult = (data) => {
    searchBox.innerHTML = '' // Clear content
    create_user_list(data, '50px', searchBox, true, true)
}
