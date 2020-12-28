**zonalStats**\
Calculates zonal statistics for a given directory with rasters and zonal features defined as a shapefile.
Exports zonal statistics as a .csv.

**Primary POCs**\
Primary setup contact (contact for any issues withi setting up the zonal stats example and running it):\
  -Caleb Pan - caleb.pan@usda.gov
 
 Primary authors (contact if any major bugs are found):
  -Caleb Pan - caleb.pan@usda.gov
  
 **Dependencies**
 -Python 3
 -rasterio
 -geopandas
 
 **Using**
 Best if used within a conda environment. In your env, install rasterio and geopandas. May need to install glob as well.
   conda install -c conda-forge rasterio
   conda install -c conda-forge geopandas
 Clone or download this repository
   Recommended: git clone https://github.com/calebpan/GTAC-Zonal-Stats.git
   If downloading, download .zip and unzip the file.
   
**Running script**
  Open zonalStats.py using the conda environment and update the following variables:
      Set the specified 'root' to your local root directory and the outtable filename.
      Set the specified 'shpfile' and 'imagedir' directories.
        E.g.
            root = r'C:/Users/cpan/GitHub/GTAC-ZS/'
            shpfile = root + 'Python/data/shps/FVS_polys.shp'
            imagedir = root + 'Python/data/images/'
            outtable = root + 'Python/data/output/zonalStats.csv'
            