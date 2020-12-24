

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

// EXTRACT VALUES AT POINTS
var outcoll = ee.FeatureCollection(snotel.map(function(ft){
    var ffstats = clipped.reduceRegion({
      reducer: ee.Reducer.median(),
      geometry: ft.geometry(),
      scale: 400,
      crs: 'EPSG:4326'
    });
    var name = ft.get('STID');
    var stats = ee.Feature(null, {
      'stid': name,
      'FF': ffstats.get('Percent_Tree_Cover'),
    });
    return stats;
  }));