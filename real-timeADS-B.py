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

workspace=r"C:\Users\Hong\Documents\ArcGIS\ADS-B"
arcpy.env.workspace=workspace
arcpy.env.overwriteOutput = True
max = long(fois) + 4
arcpy.SetProgressor("step","Get real-time ADS-B data...", 0, max, 1)

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
	file = 'D:/Thales/ADS-B/coordinate/{}.csv'.format(str(time))
	data.to_csv(file, index=False)
	arcpy.SetProgressorPosition()
	arcpy.AddMessage("{}.csv".format(time))

	arcpy.SetProgressorLabel("Creating XY event")
	#layer = os.path.join(workspace,time)
	xy = arcpy.MakeXYEventLayer_management(file,"lon","lat",time)
	arcpy.FeatureClassToShapefile_conversion(time,workspace)
	arcpy.SetProgressorPosition()
	arcpy.AddMessage("Create XY event")
	
	arcpy.SetProgressorLabel("Creating tracking layer")
	tracking = "{}T".format(time)
	arcpy.MakeTrackingLayer_ta("{}.shp".format(time),tracking,"","NOT_ADJUSTED_FOR_DST","COPY_ALL_TO_MEMORY","time","yyyy-MM-dd HH:mm:ss",'','','',"callsign")
	arcpy.AddMessage("Create tracking layer")
	symbology = r"C:\Users\Hong\Documents\ArcGIS\ADS-B\template.lyr"
	arcpy.ApplySymbologyFromLayer_management(tracking, symbology)
	arcpy.AddMessage("Set symbology")
	#arcpy.FeatureClassToShapefile_conversion(tracking,workspace)
	arcpy.SetProgressorPosition()
	#arcpy.AddMessage("Create {}.shp".format(tracking))
	#arcpy.SetParameter(2, layer)
	
	"""
	arcpy.SetProgressorLabel("Adding tracking layer")
	mypath = r"Users\Hong\Documents\ArcGIS\ADS-B\map.mxd"
	mxd = arcpy.mapping.MapDocument(mypath)
	df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
	layer = arcpy.mapping.Layer(shp(tracking))
	arcpy.mapping.AddLayer(df, layer, "AUTO_ARRANGE")
	arcpy.RefreshActiveView()
	arcpy.RefreshTOC()
	mxd.save()
	x = os.startfile(mypath)
	arcpy.SetProgressorPosition()
	"""
except Exception:
	e = sys.exc_info()[1]
	arcpy.AddError(e.args[0])