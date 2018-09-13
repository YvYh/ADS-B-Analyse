from opensky_api import OpenSkyApi
import time as t
import pandas as pd
import arcpy
from datetime import datetime
import os

def shp(name):
	return "{}.shp".format(name)

def box(airport):
	return {'ZSPD':(24.8286, 34.8286, 116.481, 126.481),
	'ZSPD_google':(26.0836, 36.0836, 116.4819, 126.4819),
	'CHINA':(24.8286, 40.8286, 100.481, 125.481)
	}.get(airport, ())

api = OpenSkyApi()

l = []

fois = arcpy.GetParameterAsText(0)
airport = arcpy.GetParameterAsText(1)

for i in xrange(long(fois)):
	states = api.get_states(bbox=box(airport))
	for s in states.states:
		time = datetime.fromtimestamp(s.time_position).isoformat()
		l.append([s.callsign, s.longitude, s.latitude, s.geo_altitude, s.heading, s.icao24, time])
	t.sleep(15)
col=['callsign', 'lon','lat','geoaltitude','heading', 'icao24', 'time']
data=pd.DataFrame(l,columns=col)
data = data.drop_duplicates(subset=['callsign','lat','lon'])
time = states.time
file = 'D:/Thales/ADS-B/coordinate/{}.csv'.format(str(time))
data.to_csv(file, index=False)
arcpy.AddMessage("{}.csv".format(time))

workspace=r"C:\Users\Hong\Documents\ArcGIS\ADS-B\ADS-B.gdb"
arcpy.env.workspace=workspace
arcpy.MakeXYEventLayer_management(file,"lon","lat",time)
arcpy.FeatureClassToShapefile_conversion(time,workspace)
arcpy.arcpy.AddMessage("Create XY event")
shppath = os.path.join(workspace,shp(time))
layer=arcpy.MakeFeatureLayer_management(shppath,time)
arcpy.SetParameterAsText(2, layer)