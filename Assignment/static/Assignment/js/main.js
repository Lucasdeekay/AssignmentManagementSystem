chkbox = document.getElementById("check");

chkbox.addEventListener("click", function(){
    if (chkbox.value == "false") {
        chkbox.value = "true";
    } else {
        chkbox.value = "false";
    }
});