# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:40:16 2019

@author: cpan
"""

# =============================================================================
# Inputs: 1) a root directory
#         2) a directory with raster with predictors
#         3) feature zones as a shapefile
# 
# Outputs: a table with zonal statistics
# 
# Dependecies: rasterio, geopandas, fiona, os, glob
# 
# The input raster directory and shapefile follow the repo structure, however,
# please feel free to change and ajust these to match your own directories and
# workflow.
# =============================================================================

from rasterstats import zonal_stats
import pandas as pd
import geopandas as gpd
import timeit, fiona, rasterio
import numpy as np
import os, glob
start = timeit.default_timer()


def getnames(imagedir):
    '''
    Parameters
    ----------
    rootdir : STRING

    Returns raster directory
    -------
    varname : LIST
        returns a list of raster image basenames.

    '''
    
    varname = []
    globdir = glob.glob(imagedir + '*.tif')
    for files in globdir:
        base = os.path.basename(files)[:-4]
        varname.append(base)
    return varname

def zonalstats(array, affine, varname, shp, uniqueID):
    '''

    Parameters
    ----------
    array : 2D Array
        Input raster predictor as a 2d array.
    affine : 2D Array
        Transformed array from row/col to xy coords..
    varname : STRING
        Predictor basename (i.e. aspect).
    shp : SHP
        Shapefile polygon to be used as the zonal features.
    uniqueID : STRING
        Unique ID for each feature in the shapefile.

    Returns
    -------
    df : Dataframe
        Output Zonal Stats table as a Pandas DF.

    '''
    rastermean, rasterstd,rastermedian = [],[],[]
    idval= []
    with fiona.drivers():
        with fiona.open(shpfile) as src:
            for feature in src:
                idval.append(feature['properties'][uniqueID])
               # settingid.append(feature['properties']['SETTING_ID'])
                poly = feature['geometry']
                refmean = zonal_stats(poly, array, affine = affine,\
                                      stats=['mean','median','std'])
                rastermean.append(refmean[0]['mean']) 
                rasterstd.append(refmean[0]['std'])
                rastermedian.append(refmean[0]['median'])
    df = pd.DataFrame({uniqueID:idval,\
                       varname + '_mean':rastermean,\
                       varname + '_median':rastermedian,\
                       varname + '_std':rasterstd})
    return df    
    del array, affine, shp ##delete the input raster to save memory  

# =============================================================================
# SET ROOT DIRECTORIES, VARIABLES, SHAPEFILES
# =============================================================================   

root = '<local directory>' ##cloned repo dir (r'C:/Users/cpan/GitHub/GTAC-ZS/')


shpfile = root + 'Python/data/shps/FVS_polys.shp'
outtable = root + 'Python/data/output/zonalStats.csv'
imagedir = root + 'Python/data/images/'

varname = getnames(imagedir)

## The column that defines each features unique ID
uniqueID = 'SPATIAL_ID'

## Set to True if you want to export the Zonal Stats Table, otherwise False
export = False

# =============================================================================
# OPEN SHP USING GEOPANDAS
# =============================================================================
data = gpd.read_file(shpfile)
statsdf = pd.DataFrame()

for var in varname:
    filename = imagedir + var + '.tif'
    print(filename)    
    raster = rasterio.open(filename)
    array = raster.read(1).astype(np.float)
    affine = raster.transform
    shp = data.copy()
    rasterstats = zonalstats(array, affine, var, shp, uniqueID)
    statsdf = pd.concat([statsdf, rasterstats], axis = 1)
    del raster, array, affine
    
statsdf = statsdf.loc[:,~statsdf.columns.duplicated()]
stop = timeit.default_timer()
print('TIME: ', round(stop-start,2))

if export == True:
    statsdf.to_csv(outtable)


