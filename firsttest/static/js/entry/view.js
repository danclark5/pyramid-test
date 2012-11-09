$(document).ready(function(){
  $("#delete_entry").submit(function(){
    delete_entry = confirm("Are you sure that this entry should be deleted");
    if (delete_entry==false)
      return false
    });
});
