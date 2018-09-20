from opensky_api import OpenSkyApi
import time as t
import pandas as pd
import arcpy
from datetime import datetime
import os

def shp(name):
	return "\{}.shp".format(name)

def box(airport):
	return {'ZSPD':(24.8286, 34.8286, 116.481, 126.481),
	'ZSPD_google':(26.0836, 36.0836, 116.4819, 126.4819),
	'CHINA':(24.8286, 41.4286, 98.081, 125.081)
	}.get(airport, ())

api = OpenSkyApi()
workspace=r"C:\Users\Hong\Documents\ArcGIS\ADS-B"
shp_folder=r"C:\Users\Hong\Documents\ArcGIS\ADS-B\shp"
csv_folder="D:/Thales/ADS-B/coordinate"

l = []

fois = arcpy.GetParameterAsText(0)
airport = arcpy.GetParameterAsText(1)


arcpy.env.workspace=workspace
arcpy.env.overwriteOutput = True
max = long(fois) + 1
arcpy.SetProgressor("step","Get real-time ADS-B data...", 0, max, 1)

states = api.get_states(bbox=box(airport))
t.sleep(10)
for i in xrange(long(fois)):
	states = api.get_states(bbox=box(airport))
	arcpy.SetProgressorLabel("Loading {}".format(i))
	for s in states.states:
		time = datetime.fromtimestamp(s.time_position).isoformat()
		l.append([s.callsign, s.longitude, s.latitude, s.geo_altitude, s.heading, s.icao24, time])
	t.sleep(15)
	arcpy.SetProgressorPosition()

try:
	arcpy.SetProgressorLabel("Saving to {}.csv".format(time))
	col=['callsign', 'lon','lat','geoaltitude','heading', 'icao24', 'time']
	data=pd.DataFrame(l,columns=col)
	data = data.drop_duplicates(subset=['callsign','lat','lon'])
	time = states.time
	#time = datetime.fromtimestamp(time).isoformat()
	file = csv_folder+"/{}.csv".format(str(time))
	data.to_csv(file, index=False)
	arcpy.SetProgressorPosition()
	arcpy.AddMessage("{}.csv".format(time))

	arcpy.SetProgressorLabel("Creating XY event")
	#layer = os.path.join(workspace,time)
	arcpy.MakeXYEventLayer_management(file,"lon","lat",time)
	arcpy.FeatureClassToShapefile_conversion(time,shp_folder)
	arcpy.SetProgressorPosition()
	arcpy.AddMessage("Create XY event")
	
	shppath = shp_folder+shp(time)
	arcpy.MakeFeatureLayer_management(shppath,time)
	
except Exception:
	e = sys.exc_info()[1]
	arcpy.AddError(e.args[0])