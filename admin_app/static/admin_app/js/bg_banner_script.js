

function bgType(){
    var bg_photo = document.getElementById('bg_photo')
    var bg_simple = document.getElementById('bg_simple')

    if (arguments[0] == bg_photo){
        bg_simple.checked = false
    }else if(arguments[0] == bg_simple){
        bg_photo.checked = false
    }

    if (bg_photo.checked){
        document.getElementById('bg_color').value = '#000000'
        document.getElementById('photo_background').style = "display: block;"
        document.getElementById('simple_background').style = "display: none;"
        bg_simple.checked = false
    } else if (bg_simple.checked){
        document.getElementById('simple_background').style = "display: block;"
        document.getElementById('photo_background').style = "display: none;"
        bg_photo.checked = false
    }
}