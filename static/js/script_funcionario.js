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

function abrirModal(){
    const modal = document.getElementById('janela-modal')
    
    modal.classList.add('abrir')
    
    modal.addEventListener('click', (e) => {
        if(e.target.id == 'fechar' || e.target.id == 'janela-modal')
        modal.classList.remove('abrir')
    })

};

function abrirModal2(){
    const modal = document.getElementById('janela-modal2')
    
    modal.classList.add('abrir')
    
    modal.addEventListener('click', (e) => {
        if(e.target.id == 'fechar' || e.target.id == 'janela-modal2')
        modal.classList.remove('abrir')
    })

};


function fecharModal(){
    
    const card = document.getElementById('modal-msg')
     
    
    card.addEventListener('click', (e) => {
        if(e.target.id == 'fechar_card' || e.target.id == 'modal-msg' || e.target.id == 'btn-funcao')
        card.classList.add('ocultar')
    })

};

btn.addEventListener('click', toggle, false);
btn_fechar.addEventListener('click', toggle, false);

startList = function() {
    if (all&&document.getElementById) {
    navRoot = document.getElementById("menuDropDown");
    for (i=0; i<navRoot.childNodes.length; i++) {
    node = navRoot.childNodes[i];
    if (node.nodeName=="LI") {
    node.onmouseover=function() {
    this.className+=" over";
      }
      node.onmouseout=function() {
      this.className=this.className.replace
      (" over", "");
       }
       }
      }
     }
    }
    window.onload=startList;





