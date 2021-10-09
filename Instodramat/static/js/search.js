const searchbar = document.querySelector("#searchbar")

searchbar.addEventListener('input', () => {
    $.ajax({
        type: 'GET',
        url: '/community/searchajax',
        data: {
            'searchinput': searchbar.value
        },
        success: function (response) {
            console.log(response)
        }
    })
})
