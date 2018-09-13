import arcpy
workspace=r"C:\Users\Hong\Documents\ArcGIS\ADS-B"
arcpy.env.workspace=workspace
region= arcpy.GetParameterAsText(0)
expression = "\"PROVINCE\" = '{}'".format(region)
arcpy.SetParameterAsText(1,expression)
