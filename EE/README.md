# **extractRasterValuetoPoint**
Extracts raster values from a given point location. Zonal features here are defined as a point shapefile.

## **Primary POCs**
Primary setup contact (contact for any issues withi setting up the zonal stats example and running it):
  - Caleb Pan - caleb.pan@usda.gov
 
 Primary authors (contact if any major bugs are found):
  - Caleb Pan - caleb.pan@usda.gov
  
   ## **Dependencies**
 -  Earth Engine Account
 
 ## **Using**
 Best if used within the Google Earth Engine Code Editor.

- Clone or download this repository
   - Recommended: ```git clone https://github.com/calebpan/GTAC-Zonal-Stats.git```
   - If downloading, download .zip and unzip the file.
   
 ### **Running script**
 Copy extractRasterValueToPoint.js in your GEE Code Editor and import the ```SNOTEL_STATIONS.shp``` found at ```EE/data/shps/``` as an Asset. In your code import the following:
- Import your ```SNOTEL_STATION.csv as a variable named ```snotel```.
- Import an ```Image``` or ```Image Collection``` from which you want to extract values from. In this script, we'll use the ```MOD44B.006 Terra Vegetation Continuous Fields Yearly Global 250m```.
    - set the imported ```Image Collection``` to a variable called ```mod44```.
