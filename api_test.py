from opensky_api import OpenSkyApi
import time as t
import pandas as pd
import arcpy
from datetime import datetime

def shp(name):
	return "{}.shp".format(name)

api = OpenSkyApi()
ZSPD = (26.0836, 36.0836, 116.4819, 126.4819)
l = []

fois = 6
for i in xrange(long(fois)):
	states = api.get_states(bbox=ZSPD)
	for s in states.states:
		time = datetime.fromtimestamp(s.time_position).isoformat()
		l.append([s.callsign, s.longitude, s.latitude, s.geo_altitude, s.heading, s.icao24, time])
	t.sleep(30)
col=['callsign', 'lon','lat','geoaltitude','heading', 'icao24', 'time']
data=pd.DataFrame(l,columns=col)
data = data.drop_duplicates(subset=['callsign','lat','lon'])
time = states.time
file = 'D:/Thales/ADS-B/coordinate/{}.csv'.format(str(time))
data.to_csv(file, index=False)

workspace=r"C:\Users\Hong\Documents\ArcGIS\ADS-B"
arcpy.env.workspace=workspace
arcpy.MakeXYEventLayer_management(file,"lon","lat",time)
arcpy.FeatureClassToShapefile_conversion(time,workspace)
arcpy.MakeFeatureLayer_management(shp(time),time)
arcpy.MakeTrackingLayer_ta(shp(time),time,"","NOT_ADJUSTED_FOR_DST","COPY_ALL_TO_MEMORY","time","yyyy-MM-dd HH:mm:ss",'','','',"callsign")