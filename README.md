# ADS-B-Analyse  
  Python scripts to analyse **ADS-B data**  
  **ArcGIS** used  
  Data is collected through **Opensky API**  


## Python script  
#### `Analyse`: 
- organize ADS-B log file into csv file  
- allow to show its itinerary  

#### `AnalyseFlight`:  
- split ADS-B log by flight callsigh  
- save each flight log into csv file

#### `time_transfer`:  
- transfer time field into readable date type  

## ArcGIS Tool  
#### `CsvToLayer`:  
- *convert* ADS-B data csv file to arcgis feature layer  

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
- update province name for region-map  

#### `Flight_count`:  
- select the region which will be analyse  
- count flight and data number within this region in selected shapefile(ADS-B data)  
- add thie record into ATF_count table

