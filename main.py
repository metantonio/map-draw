import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import plugins

#import of functions.py
from functions import excel_GMS2UTM, save_csv

data, norte_GMS, este_GMS, coordenadas = excel_GMS2UTM()
#print(norte_GMS, este_GMS)

#Creando Mapa
myMap = folium.Map(location = coordenadas[0], zoom_start = 9, tiles='Stamen Terrain')

#Agregando marcas de posición a las coordenadas
for i in range(len(coordenadas)):
    folium.Marker(coordenadas[i],popup = (str(i)+"\n N:"+str(coordenadas[i][0])+"\n S:"+str(coordenadas[i][1]))).add_to((myMap))

#Agregando líneas entre coordenadas
folium.PolyLine(coordenadas, color="red", weight=2.5, opacity=1).add_to(myMap)

#Distintas opciones de visualizacion del mapa
folium.TileLayer('openstreetmap').add_to(myMap)
#folium.TileLayer('mapquestopen').add_to(myMap)
#folium.TileLayer('MapQuest Open Aerial').add_to(myMap)
#folium.TileLayer('Mapbox Bright').add_to(myMap)
#folium.TileLayer('Mapbox Control Room').add_to(myMap)
#folium.TileLayer('stamenterrain').add_to(myMap)
#folium.TileLayer('stamentoner').add_to(myMap)	
#folium.TileLayer('cartodbpositron').add_to(myMap)
folium.LayerControl().add_to(myMap)

#Agregando opción de mostrar coordenadas por donde va pasando el mouse
formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
plugins.MousePosition(
    position='topright',
    separator=' | ',
    empty_string='NaN',
    lng_first=True,
    num_digits=20,
    prefix='Coordinates:',
    lat_formatter=formatter,
    lng_formatter=formatter,
).add_to(myMap)

#Agregando la grilla con cada 1 grados de diferencia
lat_interval = 1
lon_interval = 1

for lat in range(-90, 91, lat_interval):
     folium.PolyLine([[lat, -180],[lat, 180]], weight=0.5).add_to(myMap)

for lon in range(-180, 181, lon_interval):
    folium.PolyLine([[-90, lon],[90, lon]], weight=0.5).add_to(myMap)

#Exportar Mapa
draw = plugins.Draw(export=True)
draw.add_to(myMap)

#Generando mapa
myMap.save('Mapa.html')
print("mapa creado como: Mapa.html")
    
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



