var btn = document.querySelector(".btn_funcao");
var btn_fechar = document.querySelector(".far");
var form = document.querySelector(".form_funcao");


function toggle(event) {

    if (form.classList.contains("aparecer")) {

        form.classList.remove("aparecer");
    } else {
        form.classList.add("aparecer")
    }

}



btn.addEventListener('click', toggle, false);
btn_fechar.addEventListener('click', toggle, false);