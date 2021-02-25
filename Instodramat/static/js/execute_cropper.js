console.log('cropper is ready')
const modalBox = document.getElementById('modal-content')
const modalImage = document.getElementById('modal-image')
const imageForm = document.getElementById('formUpload')
const input = document.getElementById('id_image')
const submitButton = document.getElementById('save-model-button')
const modalSaveButton = document.getElementById('crop-button')

const input_x = document.getElementById('id_x')
const input_y = document.getElementById('id_y')
const input_width = document.getElementById('id_width')
const input_height = document.getElementById('id_height')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

var cropped_image = null


input.addEventListener('change', ()=>{
    //get image file
    const img = input.files[0]

    //Add image to modal and show modal
    const url = URL.createObjectURL(img)
    modalImage.innerHTML = `<img src="${url}" id="image" class="img-fluid" width="90%">`
    modalBox.style.display = "block";

    //Attach cropper to image
    var $image = $('#image');

    $image.cropper({
    aspectRatio: 9 / 9,
    viewMode: 1,
    dragMode: 'move',
    crop: function(event) {
        console.log(event.detail.x);
        console.log(event.detail.y);
        console.log(event.detail.width);
        console.log(event.detail.height);
        console.log(event.detail.rotate);
        console.log(event.detail.scaleX);
        console.log(event.detail.scaleY);
  },

});
    // Get the Cropper.js instance after initialized
    var cropper = $image.data('cropper');

    modalSaveButton.addEventListener('click', ()=>{
    cropped_image = cropper.getData()
    modalBox.style.display = "none";

    })
})

submitButton.addEventListener('click', ()=>{
    console.log('HERE')
    if (cropped_image){
        input_x.value = cropped_image.x;
        input_y.value = cropped_image.y;
        input_width.value = cropped_image.width;
        input_height.value = cropped_image.height;
    }
    imageForm.submit();
})





