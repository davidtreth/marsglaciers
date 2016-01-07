#!usr/bin/env/python
# use all fields with 40 deg Mars2000 Eqcyl projection 03-08-14
# adapt to Mars HRSC image/topo layerstacks 16-07-14
# edit 12-06-14 - change list slicing of filename to [0:-4]
#adapted to python 3
#import python modules
# use 0.2 sqkm and 0.04 sqkm
# this version uses 6 band layerstacks
# this version for raw aspect rather than absolute aspect from N
from rsgislib.segmentation import segutils
import os
import sys
import glob
import math

def segment_listfields(listfields):
    for f in listfields:
        os.chdir(f)
    # read in DTM resolution from file
        tresfile = open("DTMres.txt","r")
        tres = tresfile.readlines()[0]
        tresfile.close()
        tres = int(float(tres.split("(")[1].split(",")[0]))#/size1deg
    # tell user which field we're in
        print("Field h"+f+" DTM resolution "+str(tres))
        # enter "LandSerf" directory
        os.chdir("LandSerf")
    ## Perform Segmentation ##  
    # number of clusters
        numClusters = 200
        # The minimum object size in pixels
        # use 0.2sqkm and 0.04 (40000m^2)
        minObjectSize02 = int(math.ceil(200000./(tres**2)))
        minObjectSize004 = int(math.ceil(40000./(tres**2)))
        outPath02 = "rsgis_02sqkm/"
        outPath004 = "rsgis_004sqkm/"
        # make output directories if they are needed
        os.system("mkdir -p "+outPath02)
        # only do smaller segments if DTM 125m or better
        if tres <= 125:
            os.system("mkdir -p "+outPath004)
        # sampling of the input image
        imgSampling = 1000
    # assume there is only one EqCyl lat 40 rawAsp layerstack file per directory
        inputImage = glob.glob('h'+f+'*LandSerfLayerstack_rawAsp_add9999_6band.kea')[0]     
    # output segments (clumps) image
        segmentClumps = inputImage[0:-4]+"_segmentclumps"
    # output clumps mean images
        outputMeanSegments = inputImage[0:-4]+"_meansegs"
    # temporary path
        tmpPath = "./tmp/"
    # distance threshold to prevent merging
        distThres = 1000000
    # Maximum number of iterations within Kmeans
        maxKmeanIter = 200
    # output filenames
        segmentClumps02 = segmentClumps + "_numC_"+str(numClusters)+"_minObSz_"+str(minObjectSize02)+".kea"
        outputMeanSegments02 = outputMeanSegments + "_numC_"+str(numClusters)+"_minObSz_"+str(minObjectSize02)+".kea"
        segmentClumps004 = segmentClumps + "_numC_"+str(numClusters)+"_minObSz_"+str(minObjectSize004)+".kea"
        outputMeanSegments004 = outputMeanSegments + "_numC_"+str(numClusters)+"_minObSz_"+str(minObjectSize004)+".kea"

        inputImageUpdir = "../"+inputImage                
        os.chdir(outPath02)
        segutils.runShepherdSegmentation(inputImageUpdir, segmentClumps02, outputMeanSegments02, tmpPath, "KEA", False, False, False, numClusters, minObjectSize02, distThres, None, imgSampling, maxKmeanIter)
        os.chdir('..')
        if tres <= 125:
            print("DTM resolution = {r}m".format(r=tres))
            os.chdir(outPath004)
            segutils.runShepherdSegmentation(inputImageUpdir, segmentClumps004, outputMeanSegments004, tmpPath, "KEA", False, False, False, numClusters, minObjectSize004, distThres, None, imgSampling, maxKmeanIter)
            os.chdir('..')
        os.chdir('../..')
#######
directory = os.getcwd()
print(directory)
dirList = os.listdir(directory)
dirList = [d for d in dirList if (os.path.isdir(d))]
print("All fields:")
print(dirList)
#alreadyDone = ['0022', '0037', '0248', '0266', '0280', '0365', '0368', '0376', '0383', '0394', '0397', '0416', '0424', '0427', '0451', '0453', '0466', '0469', '0478', '0479', '0506', '0508', '0528', '0533', '0544', '0550', '0558', '0988', '1201', '1210', '1232', '1241', '1258', '1312', '1316', '1317', '1351', '1391', '1395', '1412', '1428', '1429', '1446', '1450', '1461', '1468', '1483', '1498', '1523', '1526', '1528', '1545', '1550', '1578', '1600', '1607', '1628', '1629', '1644', '1887', '1937', '2159', '2181', '2195', '2197', '2210', '2220', '2224', '2247', '2279', '2287', '2312', '2345', '2356', '2359', '2386', '2387', '2400', '2403', '2430', '2441', '2460', '2466', '2475', '2493', '2494', '2501', '2508', '2510', '2515', '2526', '2527', '2529', '2530', '2538', '2540', '2541', '2550', '2595', '2596', '2609', '2612', '2613', '2625', '2631', '2638', '2639', '2640', '2644', '2660']
alreadyDone = []
dirList = [d for d in dirList if d not in alreadyDone]
segment_listfields(dirList)

