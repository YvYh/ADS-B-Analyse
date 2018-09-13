# ADS-B-Analyse
Analyse ADS-B log document

- Re-organize ADS-B log file  
- Pick-up coordinate infomation  
- Add each flight's itineary into ArcGis  
- **ArcGIS** tool allows create layer from csv file then [manually] change it to a tracking layer  

## Python script  
#### `Analyse`: 
- organize ADS-B log file into csv file  
- allow to show its itinerary  

#### `AnalyseFlight`:  
- split ADS-B log by flight callsigh  
- save each flight log into csv file


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

