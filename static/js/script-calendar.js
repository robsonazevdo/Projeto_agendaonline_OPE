//inicio calendario// 

let monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julio', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

let currentDate = new Date();
let currentDay = currentDate.getDate();
let monthNumber = currentDate.getMonth();
let currentYear = currentDate.getFullYear();
let currentHours = currentDate.getHours();

let dates = document.getElementById('dates');
var month = document.getElementById('month');
let year = document.getElementById('year');
let dia = document.getElementById('dia');



let prevMonthDOM = document.getElementById('prev-month');
let nextMonthDOM = document.getElementById('next-month');

month.innerHTML = monthNames[monthNumber];
year.innerHTML = currentYear.toString();




prevMonthDOM.addEventListener('click', () => lastMonth());
nextMonthDOM.addEventListener('click', () => nextMonth());





writeMonth(monthNumber);

function writeMonth(month) {

    for (let i = startDay(); i > 0; i--) {
        dates.innerHTML += ` <div class="calendar__date calendar__item calendar__last-days">
            ${getTotalDays(monthNumber-1)-(i-1)}
        </div>`;
    }

    for (let i = 1; i <= getTotalDays(month); i++) {
        if (i === currentDay) {
            dates.innerHTML += ` <div class="calendar__date calendar__item calendar__today">${i}</div>`;
        } else {
            dates.innerHTML += ` <div class="calendar__date calendar__item">${i}</div>`;
        }
    }


}



function getTotalDays(month) {
    if (month === -1) month = 11;

    if (month == 0 || month == 2 || month == 4 || month == 6 || month == 7 || month == 9 || month == 11) {
        return 31;

    } else if (month == 3 || month == 5 || month == 8 || month == 10) {
        return 30;

    } else {

        return anoBissexto() ? 29 : 28;
    }

}

function anoBissexto() {

    return ((currentYear % 100 !== 0) && (currentYear % 4 === 0) || (currentYear % 400 === 0));
}

function startDay() {
    let start = new Date(currentYear, monthNumber, 1);
    return ((start.getDay() - 1) === -1) ? 6 : start.getDay() - 1;
}



function lastMonth() {
    if (monthNumber !== 0) {
        monthNumber--;
    } else {
        monthNumber = 11;
        currentYear--;
    }

    setNewDate();

}

function nextMonth() {
    if (monthNumber !== 11) {
        monthNumber++;
    } else {
        monthNumber = 0;
        currentYear++;
    }

    setNewDate();

}

function setNewDate() {
    currentDate.setFullYear(currentYear, monthNumber, currentDay);
    month.innerHTML = monthNames[monthNumber];
    year.innerHTML = currentYear.toString();
    dates.innerHTML = "";
    writeMonth(monthNumber);
}


select_date = document.querySelectorAll(".calendar__date .calendar__item");
console.log(select_date);


//fim calendario//
//fim calendario//