# ADS-B-Analyse  
  Python scripts to analyse **ADS-B data**  
  **ArcGIS** used  
  Data is collected through **Opensky API**  

	Bofore use all scripts, please pay attention to the file paths used(usually the path of output file)  

## Python script   
#### `Analyse`: 
- organize ADS-B log file into csv file  
- allow to show its itinerary  

#### `AnalyseFlight`:  
- split ADS-B log by flight callsign  
- save each flight log into csv file

#### `time_transfer`:  
- transfer time field into readable date type  

## ArcGIS Tool  

### *How to use?*  
Open **ArcMap** -> choose your map -> **Geoprocessing** -> **ArcToolbox** ->  
Choose one toolbox (*preinstalled is ADS-B*) -> right click -> **Add** -> **Script ** 

#### `CsvToLayer`:  
- convert ADS-B data csv file to arcgis feature layer  

#### `real-timeADS-B`:  
- collect real-time ADS-B data within the selected zone via Opensky API  
- save it to csv  
- convert it into shapefile   

#### `SQLexpression`: 
- according to the input "region" return a sql expression which will be used in later script  

#### `Tracking_Layer`:  
- create a tracking layer based on existed shapefile 
- apply the fixed symbology  

#### `Update_province`: 
- update province name-list for region-map  

#### `Flight_count`:  
- select the region which will be analysed  
- count flight and data number within the selected region (ADS-B data)  
- add thie record into ATF_count table

