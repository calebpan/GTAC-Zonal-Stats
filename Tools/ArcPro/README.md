# **ZStats**
Calculates zonal statistics for a given directory with rasters and zonal features defined as a shapefile.
Exports zonal statistics as a .csv.

## **Primary POCs**
Primary setup contact (contact for any issues with setting up the zonal stats example and running it):
  - Caleb Pan - caleb.pan@usda.gov
 
 Primary authors:
  - Joshua Reynolds (Developed)
  - Caleb Pan (modified and maintained)
      
 ## **Dependencies**
 - Python 3
 - arcPy
 - pandas
 - ArcPro License

 ## **Using**
Best if used within your ArcPro installed conda environment. In your env, install ```pandas``` and ```arcpy``` should already be installed.
-  ```conda install -c conda-forge pandas```
-  ```conda install -c esri arcpy```
- Clone or download this repository
   - Recommended: ```git clone https://github.com/calebpan/GTAC-Zonal-Stats.git```
   - If downloading, download .zip and unzip the file.
   
### **Running tool**
- In ArcCatalog, navigate to the where your tool is located and open the tool.
- The tool GUI includes 10 input arguments, described below.
    - Input the zone features as a shapefile
    - Define the unique ID for each feature object
    - The directory where the rasters are stored
    - The set of statistics to be calculated with four options:
         - IMAGERY: mean, median, std, range
         - STRUCTURE: mean, std, range, sum
         - ELEVATION/CLIMATE: mean, std
         - CATEGORICAL: majority, minority
    - joing type, can be inner or outer
    - include or exclude zones with no data
    - convert float rasters to integer (optional)
    - define a raster conversion scale (optional)
    - define to keep or discard Count/Area fields
    - define the output csv file and location
    
    
        
