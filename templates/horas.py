
def soma_horas(data, min):
    convert_hora = data.split(':')
    soma_min = int(convert_hora[0]) * 60 + int(convert_hora[1]) + int(min)
    return '%d:%02d' % (soma_min / 60, soma_min % 60) 



d = soma_horas('23:41', '123')
print(d)