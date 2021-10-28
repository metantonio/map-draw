import math
import mpu

brng = 1.57 #Bearing is 90 degrees converted to radians.
d = 15 #Distance in km

def distanceAndAngle(latitude, longitude, angulo, distance):
    R = 6378.137 #Radius of the Earth WSG-84
    d=distance #Distance in km
    brng = math.radians(angulo)
    lat1 = math.radians(latitude) #Current lat point converted to radians
    lon1 = math.radians(longitude) #Current long point converted to radians

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    #print(lat2)
    #print(lon2)
    return lat2, lon2

def distance2points(lat1,lon1,lat2,lon2):
    dist=(mpu.haversine_distance((lat1, lon1), (lat2, lon2)))
    return dist
          
#print("New Coord: ", distanceAndAngle(10,-66,10,15))
#print("distance(km): ",distance2points(10,-66,10.132699331976822,-65.97623066728403))
##it gets 14,98 km back 
