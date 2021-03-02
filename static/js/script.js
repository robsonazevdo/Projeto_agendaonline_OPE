const nav = document.querySelector(".nav-menu");
window.addEventListener("scroll", navFix, false);
const btn = document.querySelector(".btn-cadastro");
var form = document.querySelector(".form");
var btnForm = document.querySelector(".btn-fechar");

let time = 3000,
    currentImageIndex = 0,
    images = document.querySelectorAll("#slider img")
max = images.length;

//banner rotativo//

function nextImage() {

    images[currentImageIndex].classList.remove("selected")

    currentImageIndex++

    if (currentImageIndex >= max)
        currentImageIndex = 0

    images[currentImageIndex].classList.add("selected")

}

function start() {
    setInterval(() => {
        nextImage()
    }, time)
}

window.addEventListener("load", start);
//fim banner rotativo//


function navFix() {
    if (window.pageYOffset >= 200) {

        nav.classList.add("fixoNoTopo");

    } else {
        nav.classList.remove("fixoNoTopo");
    }

}

function toggle(event) {
    console.log(form.classList.contains("aparecer"))
    if (form.classList.contains("aparecer")) {

        form.classList.remove("aparecer");
    } else {
        form.classList.add("aparecer")
    }

}

btn.addEventListener("click", toggle, false);
btnForm.addEventListener("click", toggle, false);