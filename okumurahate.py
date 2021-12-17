import math

##Coloque la frecuencia de trabajo de la onda (MHz): 
##850
##Potencia media del campo eléctrico (dBu): 
##33
##
## INFORMACION DE LA ESTACION BASE 
##
##Potencia de Transmisión (W): 
##15
##Pérdidas en el terminal (dB): 
##3.4
##Ganacia de la antena de Transmisión (dBi): 
##8
##Altura de la Antena transmisora TX (m): 
##30
##
## INFORMACION DE LA ESTACION MÓVIL 
##
##Potencia de Transmisión móvil (W): 
##1
##Pérdidas en el terminal móvil (dB): 
##0.5
##Ganacia de la antena de Transmisión móvil (dBi): 
##2.14
##Altura de la Antena receptora RX (m): 
##3
##Distancia horizontal(km): 
##8

def okumura():
    frecuencia = float(input("Coloque la frecuencia de trabajo de la onda (MHz): \n"))
    campoElectrico = float(input("Potencia media del campo eléctrico (dBu): \n"))
    #Informacion de la base
    print('\n INFORMACION DE LA ESTACION BASE \n')
    potenciaTX = float(input("Potencia de Transmisión (W): \n"))
    perdidasTX = float(input("Pérdidas en el terminal (dB): \n"))
    gananciaTX = float(input("Ganacia de la antena de Transmisión (dBi): \n"))
    alturaTX = float(input("Altura de la Antena transmisora TX (m): \n"))

    #Informacion de la estación móvil
    print('\n INFORMACION DE LA ESTACION MÓVIL \n')
    potenciaRX = float(input("Potencia de Transmisión móvil (W): \n"))
    perdidasRX = float(input("Pérdidas en el terminal móvil (dB): \n"))
    gananciaRX = float(input("Ganacia de la antena de Transmisión móvil (dBi): \n"))
    alturaRX = float(input("Altura de la Antena receptora RX (m): \n"))
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
            correccion = 8.29*math.pow((math.log(1.54*alturaRX,10)),2)-1.1
            lUrbano = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
        else:
            correccion = 3.2*math.pow((math.log(11.75*alturaRX,10)),2)-4.97
            lUrbano = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
    if(option==3):
        if(frecuencia<=300):
            correccion = 8.29*math.pow((math.log(1.54*alturaRX,10)),2)-1.1
            ld = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
        else:
            correccion = 3.2*math.pow((math.log(11.75*alturaRX,10)),2)-4.97
            ld = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
        lUrbano = ld -2*math.pow(2*math.log(frecuencia/28,10),2)-5.4
    if(option==4):
        if(frecuencia<=300):
            correccion = 8.29*math.pow((math.log(1.54*alturaRX,10)),2)-1.1
            ld = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
        else:
            correccion = 3.2*math.pow((math.log(11.75*alturaRX,10)),2)-4.97
            ld = 69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion+(44.9-6.55*math.log(alturaTX,10)*math.log(distancia,10))
        lUrbano = ld -2*math.pow(4.78*math.log(frecuencia),2)+18.33*math.log(frecuencia,10)-40.94

    #resultados

    print('\n Factor de Corrección (dB): ', correccion)
    potenciaBase = 10*math.log(potenciaTX/(0.001),10)
    print("\n Potencia estacion base (dBm): ", potenciaBase)

    potenciaAparente = potenciaBase - perdidasRX +gananciaTX
    print("\n Potencia aparente PRA (dBm): ", potenciaAparente)

    lUrbano2 = potenciaAparente - campoElectrico + 20*math.log(frecuencia,10)+79.4
    print("\n Pérdidas urbanas Lurbano2 (dB): ", lUrbano2)
    print('\n Pérdida urbanas Lurbano (dB): ', lUrbano)

    Efs = 106.9-20*math.log(distancia,10)
    print('\n Intensidad de campo en espacio libre para una p.r.a de 1 kW y la distancia propuesta (dB/m): ', Efs)

    distanciaCobertura = math.pow(10,(lUrbano2-69.55+26.16*math.log(frecuencia,10)-13.82*math.log(alturaTX,10)-correccion)/(44.9-6.5*math.log(alturaTX,10)))
    print('\n Distancia de cobertura (km):', distanciaCobertura)
    return lUrbano

okumura()

