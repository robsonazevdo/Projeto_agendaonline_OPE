function somar_min(hora, carac, min ){
    var separator = hora.split(carac);
    var soma_min = parseInt(separator[0]) * 60 + parseInt(separator[1]) + parseInt(min);

    var hora = soma_min / 60 | 0;
    var minuto = soma_min % 60;
    var result = hora.toString() + ':' + minuto.toString(), hora
    return result
};

console.log(somar_min('10:20',':', '120'))