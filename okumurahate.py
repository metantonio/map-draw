import math

def okumura():
    frecuencia = float(input("Coloque la frecuencia de la onda (MHz): \n"))
    alturaRX = float(input("Altura de la Antena receptora RX (m): \n"))
    alturaTX = float(input("Altura de la Antena transmisora TX (m): \n"))
    distancia = float(input("Distancia horizontal(km): \n"))
    print("""
    Condiciones del entorno:

    1) Ciudades pequenas o medianas
    2) Ciudades grandes
    3) Zonas Sub-urbanas
    4) Zona rurales
    \n
    """)

    option=int(input('Escoja una condicion de entorno: \n'))
    if(option==1):
        correccion = (1.1*math.log(frecuencia,10)-0.7)*alturaRX-(1.56*math.log(frecuencia,10)-0.8)
        lUrbano = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
    if(option==2):
        if(frecuencia<=300):
            correccion = 8.29*(math.log(1.54*alturaRX,10))*2-1.1
            lUrbano = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
        else:
            correccion = 3.2*(math.log(11.75*alturaRX,10))*2-4.97
            lUrbano = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
    if(option==3):
        if(frecuencia<=300):
            correccion = 8.29*(math.log(1.54*alturaRX,10))*2-1.1
            ld = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
        else:
            correccion = 3.2*(math.log(11.75*alturaRX,10))*2-4.97
            ld = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
        lUrbano = ld -2*math.pow(2*math.log(frecuencia/28,10),2)-5.4
    if(option==4):
        if(frecuencia<=300):
            correccion = 8.29*(math.log(1.54*alturaRX,10))*2-1.1
            ld = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
        else:
            correccion = 3.2*(math.log(11.75*alturaRX,10))*2-4.97
            ld = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
        lUrbano = ld -2*math.pow(4.78*math.log(frecuencia),2)+18.33*math.log(frecuencia,10)-40.94
    print('\n Pérdida: ', lUrbano)

    Efs = 106.9-20*math.log(distancia,10)
    print('\n Intensidad de campo en espacio libre para una p.r.a de 1 kW: ', Efs)
    return lUrbano

okumura()

