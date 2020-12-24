// Caleb G. Pan
// RedCastle Resources, Inc.
// Salt Lake City, UT
// caleb.pan@usda.gov
// THE PURPOSE OF THIS SCRIPT IS TO EXTRACT RASTER VALUES TO A POINT.
// THE POINTS ARE INPUTS AS A CSV STORED AS AN ASSET AND THE RASTER 
// CAN BE ANY. IN THIS EXAMPLE, THE RASTER IS FRACTIONAL FOREST COVER

//var snotel = users/calebpan/Assets/SNOTEL.csv

var mod44 = ee.ImageCollection('MOD44B.006 Terra Vegetation Continuous Fields Yearly Global 250m')
var tc = mod44.select(0)// SELECT PERCENT TREE COVER (BAND)
print(tc)

var listOfImages = tc.toList(tc.size());
print(listOfImages)

var img = ee.Image(listOfImages.get(15)) // SELECT THE MOST RECENT YEAR
print(img);
print(snotel);

var clipped = img.clip(extent);
print(clipped,'clipped');
Map.addLayer(snotel);
Map.addLayer(clipped);

var ptid = 'STID'
var rastervar = 'FF'
var rasterproperty = 'Percent_Tree_Cover'

// EXTRACT VALUES AT POINTS
var outcoll = ee.FeatureCollection(snotel.map(function(ft){
    var rasterstats = clipped.reduceRegion({
      reducer: ee.Reducer.median(),
      geometry: ft.geometry(),
      scale: 400,
      crs: 'EPSG:4326'
    });
    var name = ft.get(ptid);
    var stats = ee.Feature(null, {
      ptid: name,
      rastervar: rasterstats.get(rasterproperty),
    });
    return stats;
  }));

print(outcoll,'df');
Export.table.toDrive(outcoll);