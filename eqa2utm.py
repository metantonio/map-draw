from pyproj import Proj

#An arbitral point in EQA coordinate
longitud=-66.80  #[deg.]
latitud=9.95  #[deg.]


##Calcular UTM zone
def gms2utm(lat,lon):
    #"int": Extract only integer value
    #31: Offset for UTM zone definition
    #6: Angle in a UTM zone for the longitude direction
    e2u_zone=int(divmod(lon, 6)[0])+31

    #Define EQA2UTM converter
    e2u_conv=Proj(proj='utm', zone=e2u_zone, ellps='WGS84')
    #Apply the converter
    utmx, utmy=e2u_conv(lon, lat)
    #Add offset if the point in the southern hemisphere
    if lat<0:
        utmy=utmy+10000000
        
##    print(" UTM zona/huso es ", e2u_zone, " \n", \
##          "UTM Norte es", utmy, "[m]\n",\
##          "UTM Este is ", utmx, "[m]")
    return utmy, utmx, e2u_zone
#El siguiente print es para comprobacion de la función
#print("(Norte, Este, Huso): ",gms2utm(latitud, longitud))



#Calcular Grados desde coordenadas UTM:
def utm2gms(norte,este,huso):
    if (norte>=0):
        hemi='N'
    else:
        hemi='S'
    #Add offset if the point in the southern hemisphere
    if hemi=='S':
        norte=norte-10000000
        
    #Define coordinate converter
    e2u_conv=Proj(proj='utm', zone=huso, ellps='WGS84')
    #Convert UTM2EQA
    lon, lat=e2u_conv(este, norte, inverse=True)
        
##    print("Longitude is ",lon," [deg.] \n",\
##          "Latitude is ", lat, "[deg.]")
    return lat, lon
#El siguiente print es para comprobacion de la función
#print("(latitud, longitud)",utm2gms(1100684.760966216,741202.998730454,19))
    
