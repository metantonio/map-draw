import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import plugins
from folium.plugins import MeasureControl, MiniMap
import mpu
#import io
#from PIL import Image

#import of functions.py
from functions import excel_Localizacion, save_csv, excel_Linea, excel_Circulo
from eqa2utm import gms2utm, utm2gms

#Agregando opción de mostrar coordenadas por donde va pasando el mouse
def formatoMouse(my_map):
    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
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

#Menú de Bienvenida
print("""\n Bienvenidos al Script mapa-draw.

Menú:

1-. Dibujar Puntos de Localización
2-. Dibujar Polilínea
3-. Dibujar Círculos
4-. Dibujar Puntos de Localizacion, Polilíneas y Círculos al mismo tiempo. Y transformar coordenadas a UTM
5-. Transformar Coordenadas Grado a Coordenadas UTM
6-. Salir
""")

user=int(input("\n Elige una opción \n"))

if (user==1):    
    data, norte_GMS, este_GMS, coordenadas = excel_Localizacion()
    #print(norte_GMS, este_GMS)

    #Creando Mapa
    myMap = folium.Map(location = coordenadas[0], zoom_start = 10, tiles='Stamen Terrain', control_scale=True)

    #Agregando marcas de posición a las coordenadas
    for i in range(len(coordenadas)):
        folium.Marker(coordenadas[i],popup = (str(i)+"\n N:"+str(coordenadas[i][0])+"\n E:"+str(coordenadas[i][1]))).add_to((myMap))

    
    
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
    data, norte_GMS, este_GMS, coordenadas = excel_Localizacion()
    data, norte_GMSL, este_GMSL, coordenadasL = excel_Linea()
    data, norte_GMSC, este_GMSC, coordenadasC, radio = excel_Circulo()
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

    with pd.ExcelWriter('resultsUTM.xlsx', mode='w') as writer:
        df.to_excel(writer, sheet_name="LOCALIZACION")
        df2.to_excel(writer, sheet_name="LINEA")
        df3.to_excel(writer, sheet_name="CIRCULO")
    print("\n Guardada la transformacion de coordenadas en: resultsUTM.xlsx")
    
    #Agregando marcas de posición a las coordenadas
    for i in range(len(coordenadas)):
        folium.Marker(coordenadas[i],popup = (str(i)+"\n N:"+str(coordenadas[i][0])+"\n E:"+str(coordenadas[i][1]))).add_to((myMap))

    #Agregando líneas entre coordenadas
    dist=[]
    for i in range(len(este_GMSL)-1):
        #print(i)
        dist.append(mpu.haversine_distance((norte_GMSL[int(i)], este_GMSL[int(i)]), (norte_GMSL[int(i)+1], este_GMSL[int(i)+1])))
    print("\n distancias entre vértices de la polilínea (km): ",dist)
    folium.PolyLine(coordenadasL, color="red", weight=2.5, opacity=1, popup="Distancias entre vértices en kilómetros: \n"+str(dist)).add_to(myMap)

    #Agregando círculos en las coordenadas
    for i in range(len(coordenadasC)):
        folium.Circle(coordenadasC[i], radius=radio[i], popup = (str(i)+"\n Centro es: \n N:"+str(coordenadasC[i][0])+"\n E:"+str(coordenadasC[i][1])+"\n Radio(m):"+str(radio[i])), line_color='#3186cc',fill_color='#3186cc', fill=True).add_to((myMap))

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
print("\n mapa creado como: Mapa.html")



#Tratando de generar imagen
#img_data = myMap._to_png(5)
#img = Image.open(io.BytesIO(img_data))
#img.save('Mapa.png')
    
#example=[]
#df_excel = pd.read_excel('data.xls', sheet_name='evaluation')
#df_excel_columnas = df_excel.columns
#print("\n Head: \n", df_excel_columnas)
#example.append(df_excel.head(1))
#print(df_excel)
#intermedia=[]
#for j in range(variables_columns):
#    intermedia.append(df_excel.iloc[0,j+1])
#example.append(intermedia)
#print(example)



