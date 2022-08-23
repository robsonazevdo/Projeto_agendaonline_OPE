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

}


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





