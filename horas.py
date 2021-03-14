from datetime import datetime, timezone



def calculaHora(inicial,final,intervalo):
    lista_h = []
    soma_horas = (int(final[:2]) * 60 + int(final[3:])) - (int(inicial[:2]) * 60 + int(inicial[3:]))
    h = int(inicial[:2]) * 60 + int(inicial[3:])
    limite = soma_horas // (int(intervalo[:2]) * 60 + int(intervalo[3:]))
   
    lista_h.append(inicial)
    for x in range(1,limite + 1):
        h += (int(intervalo[:2]) * 60 + int(intervalo[3:])) 
        convert = str(h // 60) + ":" + str(h % 60)
        lista_h.append(convert)

    return  lista_h





x = calculaHora("08:00", "19:30", "00:45")
print(x)

