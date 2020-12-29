# **zonalStats**
Calculates zonal statistics for a given directory with rasters and zonal features defined as a shapefile.
Exports zonal statistics as a .csv.

## **Primary POCs**
Primary setup contact (contact for any issues withi setting up the zonal stats example and running it):
  - Caleb Pan - caleb.pan@usda.gov
 
 Primary authors (contact if any major bugs are found):
  - Caleb Pan - caleb.pan@usda.gov
  
 ## **Dependencies**
 - Python 3
 - rasterio
 - geopandas
 
 ## **Using**
 Best if used within a conda environment. In your env, install ```rasterio``` and ```geopandas```. May also need to install ```glob```.
-  ```conda install -c conda-forge rasterio```
-  ```conda install -c conda-forge geopandas```
- Clone or download this repository
   - Recommended: ```git clone https://github.com/calebpan/GTAC-Zonal-Stats.git```
   - If downloading, download .zip and unzip the file.
   
### **Running script**
 Open zonalStats.py using the conda environment and update the following variables:\
- Set the specified 'root' to your local root directory and the outtable filename.
- Set the specified 'shpfile' and 'imagedir' directories. A sample shapefile and raster image are provided in the ```data``` folder.
  - E.g.\
            ```root = r'C:/Users/cpan/GitHub/GTAC-ZS/'```\
            ```shpfile = root + 'Python/data/shps/FVS_polys.shp'```\
            ```imagedir = root + 'Python/data/images/'```\
            ```outtable = root + 'Python/data/output/zonalStats.csv'```

### **Script workflow**
- ```getnames``` creates a list input raster basenames using the image directory as an input. The script then iterates through this new list to then calculate zonal stats. Using ```rasterio.open()``` we open each raster, covert it an array ```raster.readread(1).astype(np.float)``` and then transform the array from rows/col to xy using the ```raster.transform()```.
- Now with a raster open we can call the ```zonalstats``` function. This this function iterates through each feathure in the input shapefile, using ```fiona```. 
- The real work is being performed with ```refmean = zonal_stats(poly, array, affine = affine, stats =['mean', 'median', 'std'])```. Here, the mean, median, and std are being calcluated using the input feature and raster.
- The stats are then appended to lists along with the object id and put into a dataframe.
- Dataframes are calculated for each input raster. When multiple rasters are used, they are concatanated to the ```statsdf = pd.DataFrame()``` and is later exported to .csv using ```stats.to_csv(outtable)```.

