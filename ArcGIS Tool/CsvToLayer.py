# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Transfer csv file(splited from long-term log file) to shp file
# Created by Yvonne Yu
# ---------------------------------------------------------------------------


import arcpy
from datetime import datetime
import pandas as pd

def transfer_time(callsign):
	data = pd.read_csv(r'D:\Thales\ADS-B\coor\{}.csv'.format(callsign))
	for i in range(len(data.time)):
		time = datetime.fromtimestamp(data.time[i])
		data.time[i] = time.isoformat()
	newPath=r"D:\Thales\ADS-B\coor\NEW{}.csv".format(callsign)
	data.to_csv(newPath)
	return newPath

def shp(name):
	return "{}.shp".format(name)


#callsign="CXA817"
callsign = arcpy.GetParameterAsText(0)
csvfile=transfer_time(callsign)
#csvfile = arcpy.GetParameterAsText(0)
workspace=r"C:\Users\Hong\Documents\ArcGIS\ADS-B"
arcpy.env.workspace=workspace
arcpy.MakeXYEventLayer_management(str(csvfile),"lon","lat",callsign)
arcpy.FeatureClassToShapefile_conversion(callsign,workspace+"\shp")
arcpy.MakeFeatureLayer_management(shp(callsign),callsign)
arcpy.CheckOutExtension("tracking")
trackingLayer="{}T".format(callsign)
arcpy.MakeTrackingLayer_ta(callsign,trackingLayer,"","NOT_ADJUSTED_FOR_DST","COPY_ALL_TO_MEMORY","time","yyyy-MM-dd HH:mm:ss")