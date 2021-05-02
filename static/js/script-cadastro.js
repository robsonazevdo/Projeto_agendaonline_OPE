var password = document.querySelector(".password");
var confirmar_senha = document.querySelector(".confirmar-senha");

function validatePassworc(){

    if(password.value != confirmar_senha.value){
        confirmar_senha.setCustomValidity("Senhas diferentes!");


    }else{
        confirmar_senha.setCustomValidity("");

    }

}

password.onchange = validatePassworc;
confirmar_senha.onkeyup = validatePassworc;


