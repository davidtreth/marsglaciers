#!/usr/bin/env python
# 05-11-15
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

def popStatsSegmentsListfields(listfields, bandlist, bnamesPrefix,outPath02="rsgis_02sqkm/", outPath004 = "rsgis_004sqkm/"):
    for f in listfields:
        print("Field h"+f)
        os.chdir(f)                
        # read in DTM resolution from file
        tresfile = open("DTMres.txt","r")
        tres = tresfile.readlines()[0]
        tresfile.close()
        tres = int(float(tres.split("(")[1].split(",")[0]))
        os.chdir("LandSerf")
        inputImage = glob.glob('h'+f+'*LandSerfLayerstack_rawAsp.kea')[0]
        # use 6 band Layerstack, with raw aspect
        # the data comes from the layerstack before adding 9999
        # although the segmentation was of the layerstack + 9999
        inputImageUpdir = "../"+inputImage
        os.chdir(outPath02)
        # The output segments (clumps) image
        clumpsImg = glob.glob('h'+f+'*LandSerfLayerstack_rawAsp_add9999_6band_segmentclumps*.kea')[0]
    # print some user feedback.
        print("Populating Statistics for {imgStr}".format(imgStr=inputImage))
        print("DTM resolution {r}".format(r=tres))
        print("Clump file {c}".format(c=clumpsImg))
        populateSegmentsMeanStdDev(inputImageUpdir, clumpsImg, "", bandlist,bnamesPrefix)
        os.chdir("..")
        if tres <= 125:
            # do 4e4sqm clumps only for DTM resolution 125m or better
            os.chdir(outPath004)
            clumpsImg = glob.glob('h'+f+'*LandSerfLayerstack_rawAsp_add9999_6band_segmentclumps*.kea')[0]
            # print some user feedback.
            print("Populating Statistics for {imgStr}".format(imgStr=inputImage))
            print("DTM resolution {r}".format(r=tres))
            print("Clump file {c}".format(c=clumpsImg))
            populateSegmentsMeanStdDev(inputImageUpdir, clumpsImg, "", bandlist,bnamesPrefix)            
            os.chdir("..")
        os.chdir("../..")
###################### Populate Statistics #####################
# band name prefixes for the input bands.
bnamesPrefix = ["NDR", "DTMelev", "Slope", "Aspect","CrossScCrv","LongtCrv"]
# The number of images
numImgs = 1
bandlist = [1,2,3,4,5,6]
directory = os.getcwd()
print(directory)
dirList = os.listdir(directory)
DTMfields = [d for d in dirList if (os.path.isdir(d))]
popStatsSegmentsListfields(DTMfields, bandlist, bnamesPrefix)


################################################################
