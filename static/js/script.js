const nav = document.querySelector(".nav-menu");
window.addEventListener("scroll", navFix, false);
const btn = document.querySelector(".btn-cadastro");
var form = document.querySelector(".form");
var btnForm = document.querySelector(".btn-fechar");

function navFix() {
    if (window.pageYOffset >= 200) {

        nav.classList.add("fixoNoTopo");

    } else {
        nav.classList.remove("fixoNoTopo");
    }

}



//banner rotativo//  
let time = 3000;

let currentImageIndex = 0;
let images = document.querySelectorAll("#slider img");
let max = images.length;


function nextImage() {

    images[currentImageIndex].classList.remove("selected");

    currentImageIndex++;

    if (currentImageIndex >= max);
        currentImageIndex = 0;

    images[currentImageIndex].classList.add("selected");

}

function start() {
    setInterval(() => {
        nextImage()
    }, time);
}

window.addEventListener("load", start);
//fim banner rotativo//