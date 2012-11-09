$(document).ready(function(){

    $('form.delete_gallery').submit(function(){
        var delete_check = confirm("Are you sure you want to delete this gallery")
        if (!delete_check){
            return false;
        }
    });
});
