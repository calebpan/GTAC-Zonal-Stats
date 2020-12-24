# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:40:16 2019

@author: cpan
"""
import matplotlib.pyplot as plt
from rasterstats import zonal_stats
import pandas as pd
import geopandas as gpd
import timeit, fiona, rasterio
import numpy as np

start = timeit.default_timer()


    
# =============================================================================
# SET ROOT DIRECTORIES, VARIABLES, SHAPEFILES
# =============================================================================
'''
Get basenames of input tifs
'''
varname = ['blue', 'brightness', 'eastness', 'green']

root = r'E:\WR'
shpfile = r'E:\WR\shps\FVS_polys.shp'
uniqueID = 'SPATIAL_ID'
outtable = root + '\tcc\tables\WR_ZonalStats_ALL_VEGPOLY.csv'
export = False

def zonalstats(array, affine, varname, shp, uniqueID):
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
                       varname + '_mean_30m':rastermean,\
                       varname + '_median_30m':rastermedian,\
                       varname + '_std_30m':rasterstd})
    return df    
    del array, affine, shp ##delete the input raster to save memory   
    
# =============================================================================
# OPEN SHP USING GEOPANDAS
# =============================================================================
data = gpd.read_file(shpfile)
statsdf = pd.DataFrame()

for var in varname:
    filename = root + '\\predictors\\' + var + '.tif'
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

