import os
import time
import shutil
import arcpy
from arcpy.sa import *
import pandas as pd
from pandas import DataFrame
from collections import OrderedDict
import getpass

def getCols(stats_calc, keep_fields,name):
	if keep_fields == False:
		if stats_calc == 'STRUCTURE':
				cols = {'Model_ID': 'Model_ID', 'MEAN': 'MEAN_'+name, 'RANGE':'RNG_'+name, 'STD':'STD_'+name, 'SUM':'SUM_'+name}
		elif stats_calc == 'IMAGERY':
				cols = {'Model_ID': 'Model_ID', 'MEAN': 'MEAN_'+name, 'MEDIAN':'MED_'+name, 'RANGE':'RNG_'+name, 'STD':'STD_'+name}
		elif stats_calc == 'ELEVATION/CLIMATE':
				cols = {'Model_ID': 'Model_ID', 'MEAN': 'MEAN_'+name, 'STD':'STD_'+name}
		elif stats_calc == 'CATEGORICAL':
				cols = {'Model_ID': 'Model_ID', 'MAJORITY': 'MAJ_'+name, 'MINORITY':'MNR_'+name}
	else:
		if stats_calc == 'STRUCTURE':
				cols = {'Model_ID': 'Model_ID', 'COUNT_x':'COUNT', 'AREA_x':'AREA','MEAN': 'MEAN_'+name, 'RANGE':'RNG_'+name, 'STD':'STD_'+name, 'SUM':'SUM_'+name}
		elif stats_calc == 'IMAGERY':
				cols = {'Model_ID': 'Model_ID','COUNT_x':'COUNT', 'AREA_x':'AREA','MEAN': 'MEAN_'+name, 'MED':'MEDIAN_'+name, 'RANGE':'RNG_'+name, 'STD':'STD_'+name}
		elif stats_calc == 'ELEVATION/CLIMATE':
				cols = {'Model_ID': 'Model_ID','COUNT_x':'COUNT', 'AREA_x':'AREA', 'MEAN': 'MEAN_'+name, 'STD':'STD_'+name}
		elif stats_calc == 'CATEGORICAL':
				cols = {'Model_ID': 'Model_ID', 'COUNT_x':'COUNT', 'AREA_x':'AREA','MAJORITY': 'MAJ_'+name, 'MINORITY':'MNR_'+name}
	return cols

class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "Zonal Stats Tool"
		self.alias = "ZonalStatsTool"

		# List of tool classes associated with this toolbox
		self.tools = [ZonalStats]


class ZonalStats(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Multi-Variate Zonal Statistics as Table"
		self.description = "Summarizes the values of a raster(s) within the zones of a feature layer and reports the results to a table. Must be run through ArcPro, requires dbfread python package install."
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""

		# 1st parameter
		param0 = arcpy.Parameter(
		    displayName="Input Zone Features",
		    name="in_zone_features",
		    datatype="GPFeatureLayer",
		    parameterType="Required",
		    direction="Input")

		# 2nd parameter
		param1 = arcpy.Parameter(
		    displayName="Unique ID Field",
		    name="unique_id_field",
		    datatype="Field",
		    parameterType="Required",
		    direction="Input")

		param1.parameterDependencies = [param0.name]

		# 3rd parameter
		param2 = arcpy.Parameter(
		    displayName="Raster Directory",
		    name="raster_directory",
		    datatype="DEFolder",
		    parameterType="Required",
		    direction="Input")

		# 4th parameter
		param3 = arcpy.Parameter(
		    displayName="Select Statistics",
		    name="Subset_Statistics_to_Export",
		    datatype="GPString",
		    parameterType="Required",
		    direction="Input")

		param3.filter.type = "ValueList"
		param3.filter.list = ["IMAGERY", "ELEVATION/CLIMATE", "STRUCTURE", "CATEGORICAL"]
		param3.value = "IMAGERY"
		
		# 5th parameter
		param4 = arcpy.Parameter(
		    displayName="Table Join Type",
		    name="table_join_type",
		    datatype="GPString",
		    parameterType="Optional",
		    direction="Input")

		param4.filter.type = "ValueList"
		param4.filter.list = ["INNER", "OUTER"]
		param4.value = "INNER"

		# 6th parameter
		param5 = arcpy.Parameter(
		    displayName="Keep Zones With No Data Pixels",
		    name="keep_zones_with_no_data",
		    datatype="GPString",
		    parameterType="Optional",
		    direction="Input")

		param5.filter.type = "ValueList"
		param5.filter.list = ["KEEP", "DISCARD"]
		param5.value = "KEEP"

		# 7th parameter
		param6 = arcpy.Parameter(
		    displayName="Convert Float Rasters to Integer (Optional)",
		    name="convert_float_to_int",
		    datatype="GPString",
		    parameterType="Optional",
		    direction="Input")

		param6.filter.type = "ValueList"
		param6.filter.list = ["CONVERT", "DON'T CONVERT"]
		param6.value = "CONVERT"

		# 8th parameter
		param7 = arcpy.Parameter(
		    displayName="Raster Conversion Scale Value (Optional)",
		    name="conversion_scale_value",
		    datatype="GPString",
		    parameterType="Optional",
		    direction="Input")

		param7.filter.type = "ValueList"
		param7.filter.list = ["10", "100", "1000"]
		param7.value = "100"
		
		# 9th parameter
		param8 = arcpy.Parameter(
		    displayName="Keep Count/Area Fields",
		    name="Keep_Count_Area_Fields",
		    datatype="GPString",
		    parameterType="Optional",
		    direction="Input")

		param8.filter.type = "ValueList"
		param8.filter.list = ["FALSE", "TRUE"]
		param8.value = "FALSE"
		
		# 10th parameter
		param9 = arcpy.Parameter(
		    displayName="Output Table",
		    name="output_table",
		    datatype="DEFile",
		    parameterType="Required",
		    direction="Output")
		param9.filter.list = ["csv"]

		params = [param0, param1, param2, param3, param4, param5, param6, param7, param8, param9]
		return params

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""
		return True

	def updateParameters(self, parameters):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parameter
		has been changed."""
		return

	def updateMessages(self, parameters):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		return

	def execute(self, parameters, messages):
		"""The source code of the tool."""

		#========================
		# USER ARGS
		#========================

		zones = parameters[0].valueAsText
		unique_field = parameters[1].valueAsText
		raster_path = parameters[2].valueAsText
		stats_calc = parameters[3].valueAsText
		join_type = parameters[4].valueAsText
		keep_zones_with_no_data = parameters[5].valueAsText
		integerize_floats = parameters[6].valueAsText
		scale_factor = int(parameters[7].valueAsText)
		keep_fields = parameters[8].valueAsText
		out_csv = parameters[9].valueAsText
		out_path = os.path.dirname(out_csv)
		stat = 'ALL'
		#========================
		# RUN ZONAL STATS
		#========================
		
		# Get zone count
		zone_count = int(arcpy.GetCount_management(zones)[0])
		
		# Set the no data parameter
		if keep_zones_with_no_data == 'KEEP': no_data_param = 'DATA'
		else: no_data_param = 'NODATA'

		# Set the integerize floats parameter
		if integerize_floats == 'CONVERT': integerize_floats_param = True
		else: integerize_floats_param = False

		# Create temp processing directory
		temp_dir = os.path.join(out_path, 'temp_zstat_{}'.format(time.strftime('%Y%m%d_%H%M%S',time.localtime())))
		if not os.path.exists(temp_dir):
			os.makedirs(temp_dir)

		arcpy.AddMessage("Running Zonal Stats on {} segments...".format(arcpy.GetCount_management(zones)))
		arcpy.env.overwriteOutput = True

		# Get list of rasters to obtain stats for
		arcpy.env.workspace = raster_path
		rasters = arcpy.ListRasters()
		
		# Exclude crf files from calculations if
		rasters = [raster for raster in rasters if '.crf' not in raster]
		
		if stats_calc == "IMAGERY": outstats = [unique_field,"RANGE", "MEAN", "MEDIAN", "STD"]
		elif stats_calc == "STRUCTURE": outstats = [unique_field,"RANGE", "MEAN", "STD", "SUM"]
		elif stats_calc == "ELEVATION/CLIMATE": outstats = [unique_field,"MEAN", "STD"]
		elif stats_calc == "CATEGORICAL": outstats = [unique_field,"MAJORITY", "MINORITY"]

		# Create container for output dbfs
		out_dbfs = []
		
		# End processing if no rasters are present
		if len(rasters) < 1:
			arcpy.AddError("Error: No supported raster types in provided folder.")

		for raster in rasters:

			# Get some raster metadata
			raster_describe_obj = arcpy.Describe(raster)
			number_of_bands = raster_describe_obj.bandCount
			band_prefix = raster_describe_obj.children[0].name.split("_")[0]

			out_raster_name = raster.split(".")[0]
			arcpy.AddMessage("Working on {} ({} bands)...\n".format(raster, number_of_bands))

			if number_of_bands > 1:
				for band in range(1, number_of_bands + 1):

					# Get the band as a raster object
					raster_band = arcpy.Raster(os.path.join(raster, "{0}_{1}".format(band_prefix, band)))

					# Get the band data type
					band_data_type = str(arcpy.Describe(raster_band).pixelType)

					# Form the output table name
					out_table_name = os.path.join(temp_dir, "{0}_band_{1}.dbf".format(out_raster_name + '_' + stat, band))
					out_dbfs.append(out_table_name)

					# Convert float to int, if conditions are met
					if band_data_type in ['F32', 'F64'] and integerize_floats_param == True:

						arcpy.AddMessage('Converting Float Raster to Integer...')
						converted_raster_band = Int(Times(raster_band, scale_factor))

						# Run zonal stats
						ZonalStatisticsAsTable(zones, unique_field, converted_raster_band, out_table_name, no_data_param, stat)
						#arcpy.DeleteFeatures_management(converted_raster_band)
						
					else:
						# Run zonal stats
						ZonalStatisticsAsTable(zones, unique_field, raster_band, out_table_name, no_data_param, stat)
						arcpy.DeleteFeature_management(raster_band)
			else:
				# Get the raster data type
				raster_data_type = str(arcpy.Describe(raster).pixelType)

				# Form the output table name
				out_table_name = os.path.join(temp_dir, "{0}.dbf".format(out_raster_name + '_' + stat))
				out_dbfs.append(out_table_name)
	
				# Convert float to int, if conditions are met
				if raster_data_type in ['F32', 'F64'] and integerize_floats_param == True:
					arcpy.AddMessage("Converting {} to int)...\n".format(raster))
					converted_raster = Int(Times(raster, scale_factor))

					# Run zonal stats
					ZonalStatisticsAsTable(zones, unique_field, converted_raster, out_table_name, no_data_param, stat)
					#arcpy.DeleteFeature_management(converted_raster)
				else:
					# Run zonal stats
					ZonalStatisticsAsTable(zones, unique_field, raster, out_table_name, no_data_param, stat)
					#arcpy.DeleteFeature_management(raster)

		arcpy.AddMessage("Zonal Stats calculation finished...")

		#========================
		# MERGE TABLES
		#========================

		# Create empty master dataframe
		arcpy.AddMessage("Merging Tables...")
		
		# Create empty dictionary
		csvfiles = []
		# Loop through stored dbf paths and convert to csvs
		for dbf in out_dbfs:
			
			# Get zone count
			dbf_zone_count = int(arcpy.GetCount_management(dbf)[0])
			
			# Alert user if mismatching amount of zones
			if dbf_zone_count != zone_count:
				count_message = "Warning: Number of rows in zstat table for {0} is {1}, the # of input zones is {2}. Please ensure datasets overlap.".format(zone_count, dbf_zone_count, zone_count)
				arcpy.AddMessage(count_message)
			
			# Convert dbf to csv - Pandas is not smart enough to read dbf
			csv = dbf.replace(".dbf", ".csv")
			arcpy.TableToTable_conversion(dbf, temp_dir, os.path.basename(csv))
			
			csvfiles.append(csv)

		if keep_fields == 'TRUE':
			outstats.append('COUNT')
			outstats.append('AREA')
			
		tab = pd.read_csv(csvfiles[0], usecols = outstats)
		name = os.path.basename(csvfiles[0])[:-8]
		cols = getCols(stats_calc, keep_fields,name)
		tab = tab.rename(columns = cols)

		for csv in csvfiles[1:]:
			name = os.path.basename(csv)[:-8]
			df = pd.read_csv(csv, usecols = outstats)
			dfcols = getCols(stats_calc,keep_fields, name)
			df = df.rename(columns = dfcols)
			print(dfcols, name)
			if join_type == 'INNER':
				tab = tab.merge(df, left_on = unique_field, right_on = unique_field, how = 'inner')
			if join_type == 'OUTER':
				tab = tab.merge(df, left_on = unique_field, right_on = unique_field, how = 'outer')

			arcpy.AddMessage("Merging table created from {}...\n".format(name))
		exportcols = list(tab.columns.values)
		
		for cols in exportcols:
			if integerize_floats == "CONVERT":
				if cols.startswith(unique_field) | cols.startswith('COUNT') | cols.startswith('AREA'):
					pass
				else:
					arcpy.AddMessage("Rounding Mean and STD columns...")
					if cols.startswith('STD') or cols.startswith('MEAN'):
						tab[cols] = tab[cols].round(decimals = 2)
			else:
				if cols.startswith(unique_field) | cols.startswith('COUNT') | cols.startswith('AREA'):
					pass
				arcpy.AddMessage("Rounding all stat columns...")
				tab[cols] = tab[cols].round(decimals = 2)					

		arcpy.AddMessage("Tables merged!")
		tab.to_csv(out_csv, index=False) 

		#=====================================
		# Clean-up
		#====================================

		# Delete temporary working directory
		try: shutil.rmtree(temp_dir)
		except: arcpy.AddWarning("Warning: Script was successful. However, some temporary files may not have been removed.")

		return