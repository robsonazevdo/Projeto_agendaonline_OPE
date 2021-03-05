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

//banner rotativo//
let time = 3000,

    currentImageIndex = 0,
    images = document.querySelectorAll("#slider img")
max = images.length;


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



//inicio calendario// 

let monthNames = ['Janeiro', 'Fevereiro', 'Março', 'April', 'Maio', 'Junho', 'Julio', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

let currentDate = new Date();
let currentDay = currentDate.getDate();
let monthNumber = currentDate.getMonth();
let currentYear = currentDate.getFullYear();

let dates = document.getElementById('dates');
var month = document.getElementById('month').innerHTML = monthNames[monthNumber];
let year = document.getElementById('year').innerHTML = currentYear.toString();

let prevMonthDOM = document.getElementById('prev-month');
let nextMonthDOM = document.getElementById('next-month');


//fim calendario//