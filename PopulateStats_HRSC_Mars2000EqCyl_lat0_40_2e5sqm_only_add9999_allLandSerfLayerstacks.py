#!/usr/bin/env python
# 03-08-14
# David Trethewey
# adapted for python 3
# Import python modules
from rsgislib import rastergis
import sys
import os.path
import glob
import time
def populateSegmentsMeanStdDev(inputImage, clumpsImg, colNamePrefix, bandlist, bandnames):
	"""
	A function to populate mean and standard deviation values as
	columns within the attribute table for a single band image.
	"""
	# Create an empty list
	bandStats = []
	# Define the statistics to be calculated for the band and the field names
	# If the input image had mulitple image bands for which you wished to 
	# calculate statistics you need to duplicate this line and change the
	# band number and field names.
	#colNamePrefix = 'h'+colNamePrefix
	for i in range(len(bandlist)):
	#        bandStats.append(rastergis.BandAttStats(band=bandlist[i], minField = colNamePrefix+bandnames[i]+'_Min', maxField = colNamePrefix+bandnames[i]+'_Max', meanField=colNamePrefix+bandnames[i]+'_Mean',  stdDevField=colNamePrefix+bandnames[i]+'_StdDev', medianField=colNamePrefix+bandnames[i]+'_Median'))
		bandStats.append(rastergis.BandAttStats(band=bandlist[i], minField = colNamePrefix+bandnames[i]+'_Min', maxField = colNamePrefix+bandnames[i]+'_Max', meanField=colNamePrefix+bandnames[i]+'_Mean',  stdDevField=colNamePrefix+bandnames[i]+'_StdDev'))
	# Run the RSGISLib command with the input parameters.
	rastergis.populateRATWithStats(inputImage, clumpsImg, bandStats)
	#def popStatsSegmentsListfields(listfields, bandlist, bnamesPrefix,outPath02="rsgis_02sqkm/",outPath1 = "rsgis_1sqkm/", outPath2 = "rsgis_4sqkm/"):

def popStatsSegmentsListfields(listfields, bandlist, bnamesPrefix,outPath02="rsgis_02sqkm/"):
	for f in listfields:
		print("Field h"+f)
		os.chdir(f)                
		os.chdir("LandSerf")
		inputImage = glob.glob('h'+f+'*LandSerfLayerstack3.kea')[0] #use 6 band Layerstack
		inputImageUpdir = "../"+inputImage
		os.chdir(outPath02)
		clumpsImg = glob.glob('h'+f+'*LandSerfLayerstack_add9999_6band_segmentclumps*.kea')[0]
	# print some user feedback.
		print("Populating Statistics for {imgStr}".format(imgStr=inputImage))
		populateSegmentsMeanStdDev(inputImageUpdir, clumpsImg, "", bandlist,bnamesPrefix)
		os.chdir("../../..")
###################### Populate Statistics #####################
# The output segments (clumps) image
# band name prefixes for the input bands.
#bnamesPrefix_NHemisph = ["NDR", "DTMelev", "Slope", "AspectN","CrossScCrv","LongtCrv","MeanCrv","PlanCrv","ProfCrv","LandSerfFeat"]
bnamesPrefix_NHemisph = ["NDR", "DTMelev", "Slope", "AspectN","CrossScCrv","LongtCrv"]
# The number of images
numImgs = 1
#bandlist = [1,2,3,4,5,6,7,8,9,10]
bandlist = [1,2,3,4,5,6]
directory = os.getcwd()
print(directory)
dirList = os.listdir(directory)
DTMfields = [d for d in dirList if (os.path.isdir(d))]
popStatsSegmentsListfields(DTMfields, bandlist, bnamesPrefix_NHemisph)


################################################################
