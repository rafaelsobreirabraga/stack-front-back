$(document).ready(function(){
    document.addEventListener("click", function(element) {
        if ( element.target.parentElement.name == "deleteUser") {
            console.log('Set value in input : "delete_user_id" = ' + element.target.parentElement.id);
            document.getElementById("delete_user_id").value=element.target.parentElement.id
        }
    });

    $('#modal-delete-user').modal({
        onOpenEnd: function(obj, ui) {
            //console.log("onOpenEnd | objectId = " + user_id, ", UI >> " + ui);
            let link = "/user/delete/" + document.getElementById("delete_user_id").value;
            document.getElementById('modal-delete-user-yes').setAttribute('href', link);
        }
    });
});