# David Trethewey 03-08-2014
# gdal_polygonize.py on the segmentclumps files
# assume we are running from */mexhrs_2001/data directory
# under which each field is in directory XXXX
# assume filenames of form 'HXXXX_0000_da4.kea' etc.
import os.path
import sys
#from rsgislib import imageutils
from rsgislib import rastergis
import glob
import time
bnamesPrefix_NHemisph = ["NDR", "DTMelev", "Slope", "AspectN","CrossScCrv","LongtCrv"]
def gdal_poly_all(DTMfields,SHemisph=0,outPath02="rsgis_02sqkm/"):
#	if SHemisph>0:
#		bandNames_pref = bnamesPrefix_SHemisph
#	else:
#		bandNames_pref = bnamesPrefix_NHemisph
	bandNames_pref = bnamesPrefix_NHemisph
	for f in DTMfields:
		# start with the colours from the colour table
		bandNames = ['Red', 'Green', 'Blue']
		#colNamePrefix = "h"+f+"_"
		colNamePrefix = ""
		bandlist = [1,2,3,4,5,6]			
		for i in range(len(bandlist)):
			bandNames.append(colNamePrefix+bandNames_pref[i]+'_Min')
			bandNames.append(colNamePrefix+bandNames_pref[i]+'_Max')
			bandNames.append(colNamePrefix+bandNames_pref[i]+'_Mean')
			bandNames.append(colNamePrefix+bandNames_pref[i]+'_StdDev')
			# possibly median is not working on F4 Rsgislib version
			# bandNames.append(colNamePrefix+bandNames_pref[i]+'_Median')
		os.chdir(f)
		os.chdir("LandSerf")
		os.chdir(outPath02)
		clumpsImg = glob.glob('h'+f+'*LandSerfLayerstack_add9999_6band_segmentclumps*.kea')[0]
		vectorPolyFile = clumpsImg[:-4]+"_vectorpolygons.shp"
		ASCII_CSVFile = clumpsImg[:-4]+"_ASCII_RAT.csv"
		gdal_polycmd = "gdal_polygonize.py "+clumpsImg+" -f 'ESRI Shapefile' "+vectorPolyFile
		os.system(gdal_polycmd)
		rastergis.export2Ascii(clumpsImg, ASCII_CSVFile, bandNames)
		os.chdir("../../..")
directory = os.getcwd()
print(directory)
dirList = os.listdir(directory)
DTMfields = [d for d in dirList if (os.path.isdir(d))]
gdal_poly_all(DTMfields)
