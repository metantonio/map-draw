import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import plugins
from folium.plugins import MeasureControl, MiniMap, HeatMap, HeatMapWithTime, FloatImage
import mpu
import itertools
from branca.element import Template, MacroElement

#import io
#from PIL import Image

#import of functions.py
from functions import excel_Localizacion, save_csv, excel_Linea, excel_Circulo, excel_PuntoDistAng
from eqa2utm import gms2utm, utm2gms
from distAndAngle import distanceAndAngle, distance2points, distanceAndAngleInterpolation
from scaletemplate import leyenda

#Agregando opción de mostrar coordenadas por donde va pasando el mouse
def formatoMouse(my_map):
    formatter = "function(num) {return L.Util.formatNum(num, 6) + ' º ';};"
    return plugins.MousePosition(
        position='topright',
        separator=' | ',
        empty_string='NaN',
        lng_first=True,
        num_digits=20,
        prefix='Coordinates:',
        lat_formatter=formatter,
        lng_formatter=formatter,
        ).add_to(my_map)

#definicion de la grilla o grid:
def grilla():
    lat_interval = 1
    lon_interval = 1

    for lat in range(-90, 91, lat_interval):
        folium.PolyLine([[lat, -180],[lat, 180]], weight=0.5).add_to(myMap)

    for lon in range(-180, 181, lon_interval):
        folium.PolyLine([[-90, lon],[90, lon]], weight=0.5).add_to(myMap) 

#comprobacion de data vacia
def is_empty(data_structure):
    if data_structure:
        #print("No está vacía", data_structure)
        return False
    else:
        #print("Está vacía")
        return True

def heatMap(norteLista, esteLista, heatmapLista):
    data=[]
    i=0
    heat=0
    for element in norteLista:
        if heatmapLista[i]>1:
            heat=heatmapLista[i]/100
        data.append([element, esteLista[i], heat])
        i=i+1
    #print("este es la data del heatmap", data)
    return data



def menuPpal(user):
    if (user==1):    
        data, norte_GMS, este_GMS, coordenadas, colorM = excel_Localizacion()
        #print(norte_GMS, este_GMS)

        #Creando Mapa
        myMap = folium.Map(location = coordenadas[0], zoom_start = 18, tiles='Stamen Terrain', control_scale=True)

        #Agregando marcas de posición a las coordenadas
        for i in range(len(coordenadas)):
            folium.Marker(coordenadas[i], icon = folium.Icon(color=colorM[i]), popup = (str(i)+"\n N:"+str(coordenadas[i][0])+"\n E:"+str(coordenadas[i][1]))).add_to((myMap))

        
        
    if (user==2):    
        data, norte_GMSL, este_GMSL, coordenadasL = excel_Linea()
        #print(norte_GMS, este_GMS)

        #Creando Mapa
        myMap = folium.Map(location = coordenadasL[0], zoom_start = 10, tiles='Stamen Terrain', control_scale=True)

        #Agregando líneas entre coordenadas
        dist=[]
        for i in range(len(este_GMSL)-1):
            #print(i)
            dist.append(mpu.haversine_distance((norte_GMSL[int(i)], este_GMSL[int(i)]), (norte_GMSL[int(i)+1], este_GMSL[int(i)+1])))
        print("\n distancias entre vértices de la polilínea (km): ",dist)
        folium.PolyLine(coordenadasL, color="red", weight=2.5, opacity=1, popup="Distancias entre vértices en kilómetros: \n"+str(dist)).add_to(myMap)

    if (user==3):    
        data, norte_GMS, este_GMS, coordenadasC, radio = excel_Circulo()
        #print(norte_GMS, este_GMS)

        #Creando Mapa
        myMap = folium.Map(location = coordenadasC[0], zoom_start = 10, tiles='Stamen Terrain', control_scale=True)

        #Agregando círculos en las coordenadas
        for i in range(len(coordenadasC)):
            folium.Circle(coordenadasC[i], radius=radio[i], popup = (str(i)+"\n Centro es: \n N:"+str(coordenadasC[i][0])+"\n E:"+str(coordenadasC[i][1])+"\n Radio(m):"+str(radio[i])), line_color='#3186cc',fill_color='#3186cc', fill=True).add_to((myMap))

    if(user==4):
        data, norte_GMS, este_GMS, coordenadas, colorM = excel_Localizacion()
        data, norte_GMSL, este_GMSL, coordenadasL = excel_Linea()
        data, norte_GMSC, este_GMSC, coordenadasC, radio = excel_Circulo()
        data, norte_GMSP, este_GMSP, coordenadasP, anguloP, distanciaP, heatmapP = excel_PuntoDistAng()
        #print(norte_GMS, este_GMS)

        #Creando Mapa
        myMap = folium.Map(location = coordenadas[0], zoom_start = 10, tiles='Stamen Terrain', control_scale=True)

        norte_UTM=[0]*len(norte_GMS)
        este_UTM=[0]*len(norte_GMS)
        huso_UTM=[0]*len(norte_GMS)
        for i in range(len(norte_GMS)):
            norte_UTM[i], este_UTM[i], huso_UTM[i]= gms2utm(norte_GMS[i],este_GMS[i])

        df= pd.DataFrame({'Norte':norte_UTM, 'Este':este_UTM, 'Huso':huso_UTM})
        print("\n Data Localización en UTM \n",df)

        norte_UTML=[0]*len(norte_GMSL)
        este_UTML=[0]*len(norte_GMSL)
        huso_UTML=[0]*len(norte_GMSL)
        for i in range(len(norte_GMSL)):
            norte_UTML[i], este_UTML[i], huso_UTML[i]= gms2utm(norte_GMSL[i],este_GMSL[i])

        df2= pd.DataFrame({'Norte':norte_UTML, 'Este':este_UTML, 'Huso':huso_UTML})
        print("\n Data Vértices Polilínea en UTM \n",df2)

        norte_UTMC=[0]*len(norte_GMSC)
        este_UTMC=[0]*len(norte_GMSC)
        huso_UTMC=[0]*len(norte_GMSC)
        for i in range(len(norte_GMSC)):
            norte_UTMC[i], este_UTMC[i], huso_UTMC[i]= gms2utm(norte_GMSC[i],este_GMSC[i])

        df3= pd.DataFrame({'Norte':norte_UTMC, 'Este':este_UTMC, 'Huso':huso_UTMC})
        print("\n Data Vértices Polilínea en UTM \n",df3)

        ######un apartado para conseguir las coords del patrón de radiacion en grados
        norte_GMSP2=[0]*len(norte_GMSP)
        este_GMSP2=[0]*len(este_GMSP)
        dataHeatMap=[]
        #auxlist=[]
        for i in range(len(norte_GMSP)):
            norte_GMSP2[i], este_GMSP2[i] = distanceAndAngle(norte_GMSP[i],este_GMSP[i], anguloP[i], distanciaP[i])
            auxlist=distanceAndAngleInterpolation(norte_GMSP[i],este_GMSP[i], anguloP[i], distanciaP[i], heatmapP[i])
            for element in auxlist:
                dataHeatMap.append(element)
            
        df4 = pd.DataFrame({'Norte Latitud(grados)':norte_GMSP2, 'Este Longitud(grados)':este_GMSP2, 'Angulo giro (grados)':anguloP, 'Distancia (km)':distanciaP})
        print("\n Coordenadas patrón de radiacion en Grados \n",df4)
        #print('interpolacion',dataHeatMap)
                       
        norte_UTMP=[0]*len(norte_GMSP2)
        este_UTMP=[0]*len(norte_GMSP2)
        huso_UTMP=[0]*len(norte_GMSP)
        for i in range(len(norte_GMSP2)):
            norte_UTMP[i], este_UTMP[i], huso_UTMP[i]= gms2utm(norte_GMSP2[i],este_GMSP2[i])
        df5= pd.DataFrame({'Norte':norte_UTMP, 'Este':este_UTMP, 'Huso':huso_UTMP, 'Angulo giro (grados)':anguloP, 'Distancia (km)':distanciaP})
        print("\n Coordenadas patrón de radiacion en UTM \n",df5)

        ##EXPORTACION A EXCEL
        with pd.ExcelWriter('resultsUTM.xlsx', mode='w') as writer:
            df.to_excel(writer, sheet_name="LOCALIZACION")
            df2.to_excel(writer, sheet_name="LINEA")
            df3.to_excel(writer, sheet_name="CIRCULO")
            df4.to_excel(writer, sheet_name="P_DIST_ANG_G")
            df5.to_excel(writer, sheet_name="P_DIST_ANG_UTM")
        print("\n Guardada la transformacion de coordenadas en: resultsUTM.xlsx")
        
        #Agregando marcas de posición a las coordenadas de la hoja de Localizacion
        if (is_empty(coordenadas)==False):
            for i in range(len(coordenadas)):
                folium.Marker(coordenadas[i], icon = folium.Icon(color=colorM[i]), popup = (str(i)+"\n N:"+str(coordenadas[i][0])+"\n E:"+str(coordenadas[i][1]))).add_to((myMap))

        #Agregando marcas de posición a las coordenadas de la hoja de Punto_Ang_distancia
        print("\n Dibujar marcadores de localización de los vértices del perímetro de radiación?? ")
        desicion=int(input("\n 1)Sí \n 2)No \n"))
        if (desicion==1):
            for i in range(len(norte_GMSP2)):
                folium.Marker((norte_GMSP2[i],este_GMSP2[i]),popup = (str(i)+"\n N:"+str(norte_GMSP2[i])+"\n E:"+str(este_GMSP2[i]))).add_to((myMap))
        #Agregando líneas entre coordenadas
        dist=[]
        
        for i in range(len(este_GMSL)-1):
            #print(i)
            dist.append(mpu.haversine_distance((norte_GMSL[int(i)], este_GMSL[int(i)]), (norte_GMSL[int(i)+1], este_GMSL[int(i)+1])))
        if (is_empty(coordenadasL)==False):
            print("\n distancias entre vértices de la polilínea (km): ",dist)
            folium.PolyLine(coordenadasL, color="red", weight=2.5, opacity=1, popup="Longitud (km): \n"+str(dist)).add_to(myMap)

        dist=[]
        for i in range(len(este_GMSP2)-1):
            #print(i)
            dist.append(mpu.haversine_distance((norte_GMSP2[int(i)], este_GMSP2[int(i)]), (norte_GMSP2[int(i)+1], este_GMSP2[int(i)+1])))
        #print("\n distancias entre vértices de la polilínea (km): ",dist)

        #Dibujo del perimetro
        coordenadasRadiacion=[]
        print("\n Dibujar polilínea del perímetro de radiación?? ")
        desicion=int(input("\n 1)Sí \n 2)No \n"))
        if (desicion==1):
            for i in range(len(norte_GMSP2)):
                coordenadasRadiacion.append([norte_GMSP2[i],este_GMSP2[i]])
            if (is_empty(coordenadasRadiacion)==False):    
                folium.PolyLine(coordenadasRadiacion, color="red", weight=2.5, opacity=1, popup="Distancias entre vértices en kilómetros: \n"+str(dist)).add_to(myMap)
            
        #Agregando círculos en las coordenadas
        if (is_empty(coordenadasC)==False):
            for i in range(len(coordenadasC)):
                folium.Circle(coordenadasC[i], radius=radio[i], popup = (str(i)+"\n Centro es: \n N:"+str(coordenadasC[i][0])+"\n E:"+str(coordenadasC[i][1])+"\n Radio(m):"+str(radio[i])), line_color='#3186cc',fill_color='#3186cc', fill=True).add_to((myMap))

        #HEATMAP
        heatMapData=heatMap(norte_GMSP2, este_GMSP2, heatmapP)
        #dataFinal=[]
        dataFinal=[*dataHeatMap, *heatMapData]
        #dataFinal = heatMapData+dataHeatMap
        print("\n Opciones para el mapa de radiación: ")
        desicion=int(input("\n 1)Colorear Área de Radiación (Versión Recomendada) \n 2)Colorear experimental (En desarrollo) \n 3)No dibujar \n"))
        if (desicion==1):
            #HeatMap(heatMapData, name="Radiacion Externa", gradient={0.0: 'pink', 0.15: 'blue', 0.3: 'green',  0.7: 'yellow', 1: 'red'}, blur=5, radius=25, min_opacity=0.0).add_to(myMap)
            #HeatMap([[norte_GMSP[0], este_GMSP[0], 1]], name="Radiacion Centro", gradient={0.0: 'pink', 0.15: 'blue', 0.3: 'green',  0.7: 'yellow', 1: 'red'}, blur=1, radius=30, min_opacity=1.0).add_to(myMap)
            #HeatMap(dataHeatMap, name="Radiacion Interna", gradient={0.0: 'pink', 0.15: 'blue', 0.3: 'green',  0.7: 'yellow', 1: 'red'}, blur=1, radius=35, max_zoom=25).add_to(myMap)
            HeatMapWithTime([dataHeatMap], name="Radiacion E.M.", gradient={0.0: 'pink', 0.2: 'blue', 0.4: 'green',  0.7: 'yellow', 1: 'red'}, radius=50, display_index=False, min_opacity=0.4, max_opacity=0.6, position='topright').add_to(myMap)
            #legend_img = './escala-color.jpg'
            #imageScale=FloatImage(legend_img, bottom=0, left=20)
            #imageScale.layer_name="Escala de Color"
            #myMap.add_children(imageScale)
            leyenda(myMap)
            
            
        if(desicion==2):
            for element in dataFinal:
                HeatMap([element], name="test", gradient={0.0: 'pink', 0.15: 'blue', 0.3: 'green',  0.7: 'yellow', 1: 'red'}, blur=15, radius=30, min_opacity=element[2], max_zoom=12).add_to(myMap)
        
                
        #print('Puntos de Control del HeatMap: \n', dataFinal)

    #Transformacion a Coordenadas UTM:
    if(user==5):
        data, norte_GMS, este_GMS, coordenadas = excel_Localizacion()
        data, norte_GMSL, este_GMSL, coordenadasL = excel_Linea()
        data, norte_GMSC, este_GMSC, coordenadasC, radio = excel_Circulo()

        #Creando Mapa
        myMap = folium.Map(location = coordenadas[0], zoom_start = 10, tiles='Stamen Terrain', control_scale=True)

        norte_UTM=[0]*len(norte_GMS)
        este_UTM=[0]*len(norte_GMS)
        huso_UTM=[0]*len(norte_GMS)
        for i in range(len(norte_GMS)):
            norte_UTM[i], este_UTM[i], huso_UTM[i]= gms2utm(norte_GMS[i],este_GMS[i])

        df= pd.DataFrame({'Norte':norte_UTM, 'Este':este_UTM, 'Huso':huso_UTM})
        print("\n Data Localización en UTM \n",df)

        norte_UTML=[0]*len(norte_GMSL)
        este_UTML=[0]*len(norte_GMSL)
        huso_UTML=[0]*len(norte_GMSL)
        for i in range(len(norte_GMSL)):
            norte_UTML[i], este_UTML[i], huso_UTML[i]= gms2utm(norte_GMSL[i],este_GMSL[i])

        df2= pd.DataFrame({'Norte':norte_UTML, 'Este':este_UTML, 'Huso':huso_UTML})
        print("\n Data Vértices Polilínea en UTM \n",df2)

        norte_UTMC=[0]*len(norte_GMSC)
        este_UTMC=[0]*len(norte_GMSC)
        huso_UTMC=[0]*len(norte_GMSC)
        for i in range(len(norte_GMSC)):
            norte_UTMC[i], este_UTMC[i], huso_UTMC[i]= gms2utm(norte_GMSC[i],este_GMSC[i])

        df3= pd.DataFrame({'Norte':norte_UTMC, 'Este':este_UTMC, 'Huso':huso_UTMC})
        print("\n Data Vértices Polilínea en UTM \n",df3)

        with pd.ExcelWriter('resultsUTM.xlsx', mode='w') as writer:
            df.to_excel(writer, sheet_name="LOCALIZACION")
            df2.to_excel(writer, sheet_name="LINEA")
            df3.to_excel(writer, sheet_name="CIRCULO")
                    
        print("\n Guardada la transformacion de coordenadas en: resultsUTM.xlsx")
        
    #Agregar Rectángulos (con tuplas desde esquina inferior izq a esquina superior derecha)
    #folium.Rectangle(bounds=[(37.554, 126.95), (37.556, 126.97)],fill=True,color='orange', tooltip='this is Rectangle').add_to(korea)
    return myMap

def generatingMap(mapinput):
    #Distintas opciones free de visualización de mapas
    folium.TileLayer('openstreetmap').add_to(myMap)
    folium.TileLayer('Stamen Toner').add_to(myMap)
    folium.TileLayer('Stamen Watercolor').add_to(myMap)
    folium.raster_layers.TileLayer(
        tiles="http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="google",
        name="google maps",
        max_zoom=20,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
        overlay=False,
        control=True,
    ).add_to(myMap)
    folium.raster_layers.TileLayer(
        tiles="http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        attr="google",
        name="google street view",
        max_zoom=20,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
        overlay=False,
        control=True,
    ).add_to(myMap)
    folium.LayerControl().add_to(myMap)

    #Agregando la grilla con cada 1 grados de diferencia
    grilla()

    #Exportar Mapa
    #draw = plugins.Draw(export=True)
    #draw.add_to(myMap)
        

    formatoMouse(myMap)

    #Control para medición de distancias
    myMap.add_child(MeasureControl())

    #Agregando mini mapa
    minimap = MiniMap(toggle_display=True)
    myMap.add_child(minimap)

    #Generando mapa
    myMap.save('Mapa.html')
    print("""
    ###########################
    MAPA GENERADO EN: Mapa.html
    ###########################
    """)

if __name__ == '__main__':

    print("""\n Menú Principal

    Menú:

    1-. Dibujar Puntos de Localización
    2-. Dibujar Polilínea
    3-. Dibujar Círculos
    4-. Dibujar Puntos de Localizacion, Polilíneas, Círculos, y P_DIST_ANG. Y transformar coordenadas a UTM
    5-. Transformar Coordenadas Grado a Coordenadas UTM
    6-. Salir

    Creador: Antonio Martínez
    @metantonio
    """)
    userOp1=int(input("\n Elige una opción \n"))
    while userOp1<6:
        myMap=menuPpal(userOp1)
        generatingMap(myMap)
        print("""\n Regresando al Menú Principal

        Menú:

        1-. Dibujar Puntos de Localización
        2-. Dibujar Polilínea
        3-. Dibujar Círculos
        4-. Dibujar Puntos de Localizacion, Polilíneas, Círculos, y P_DIST_ANG. Y transformar coordenadas a UTM
        5-. Transformar Coordenadas Grado a Coordenadas UTM
        6-. Salir

        Creador: Antonio Martínez
        @metantonio
        
        """)
        userOp1=int(input("\n Elige una opción \n"))
        if userOp1==6:
            print('Cerrando la aplicación...')
            break

#Código creado por:
#Antonio Martínez @metantonio


