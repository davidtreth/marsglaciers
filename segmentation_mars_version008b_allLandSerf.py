#!usr/bin/env/python
# use all fields with 40 deg Mars2000 Eqcyl projection 03-08-14
# adapt to Mars HRSC image/topo layerstacks 16-07-14
# edit 12-06-14 - change list slicing of filename to [0:-4]
#adapted to python 3
#import python modules
# only 0.2 sqkm for now
# this version uses 6 band layerstacks
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
	# user interaction
		print("Field h"+f+" DTM resolution "+str(tres))
        # enter "LandSerf" directory
		os.chdir("LandSerf")
	## Perform Segmentation ##	
	# number of clusters
		numClusters = 200
    	# The minimum object size in pixels
    	# use size of 1 sq km. and 4 sq. km
        # initially 0.2sqkm
		minObjectSize02 = int(math.ceil(200000./(tres**2)))
		#minObjectSize1 = int(math.ceil(1000000./(tres**2)))
		#minObjectSize4 = int(math.ceil(4000000./(tres**2)))

		outPath02 = "rsgis_02sqkm/"
		#outPath1 = "rsgis_1sqkm/"
		#outPath4 = "rsgis_4sqkm/"
		os.system("mkdir -p "+outPath02)
		#os.system("mkdir -p "+outPath1)
		#os.system("mkdir -p "+outPath4)
    	# sampling of the input image
		imgSampling = 1000
	# assume there is only one EqCyl lat 40 layerstack file per directory
		inputImage = glob.glob('h'+f+'*LandSerfLayerstack_add9999_6band.kea')[0]		
	# output segments (clumps) image
		segmentClumps = inputImage[0:-4]+"_segmentclumps"
	# output clumps mean images
		outputMeanSegments = inputImage[0:-4]+"_meansegs"
	# temporary path
		tmpPath = "./tmp/"
	# distance threshold to prevent merging
		distThres = 1000000
#		distThres4 = 4
#		distThres3 = 3
#		distThres100 = 100
#		distThres10 = 10
#                distThres5 = 5
#                distThres2 = 2
                
	# Maximum number of iterations within Kmeans
		maxKmeanIter = 200
		segmentClumps02 = segmentClumps + "_numC_"+str(numClusters)+"_minObSz_"+str(minObjectSize02)+".kea"
		outputMeanSegments02 = outputMeanSegments + "_numC_"+str(numClusters)+"_minObSz_"+str(minObjectSize02)+".kea"

		#segmentClumps1 = segmentClumps + "_numC_"+str(numClusters)+"_minObSz_"+str(minObjectSize1)+".kea"
		#outputMeanSegments1 = outputMeanSegments + "_numC_"+str(numClusters)+"_minObSz_"+str(minObjectSize1)+".kea"

		#segmentClumps4 = segmentClumps + "_numC_"+str(numClusters)+"_minObSz_"+str(minObjectSize4)+".kea"
		#outputMeanSegments4 = outputMeanSegments + "_numC_"+str(numClusters)+"_minObSz_"+str(minObjectSize4)+".kea"

		inputImageUpdir = "../"+inputImage                
		os.chdir(outPath02)
		segutils.runShepherdSegmentation(inputImageUpdir, segmentClumps02, outputMeanSegments02, tmpPath, "KEA", False, False, False, numClusters, minObjectSize02, distThres, None, imgSampling, maxKmeanIter)
		os.chdir('..')
                #os.chdir(outPath1)
# RSGISLib function call
		#segutils.runShepherdSegmentation(inputImageUpdir, segmentClumps1, outputMeanSegments1, tmpPath, "KEA", False, False, False, numClusters, minObjectSize1, distThres, None, imgSampling, maxKmeanIter)		
                #os.chdir('..')
                #os.chdir(outPath4)
		#segutils.runShepherdSegmentation(inputImageUpdir, segmentClumps4, outputMeanSegments4, tmpPath, "KEA", False, False, False, numClusters, minObjectSize4, distThres, None, imgSampling, maxKmeanIter)
		#os.chdir('..')
		os.chdir('../..')
#######
directory = os.getcwd()
print(directory)
dirList = os.listdir(directory)
dirList = [d for d in dirList if (os.path.isdir(d))]
print("All fields:")
print(dirList)
#dirList2 = ['5306', '5314', '5317', '5321', '5322', '5324', '5328', '5335', '5339', '5340', '5342', '5360', '5376', '5378', '5380', '5383', '5401', '6395', '6408', '6409', '6419', '6437', '6465', '6486', '6544', '6552', '0506', '1428', '1937', '2441', '2613', '3283', '5299', '5405']
segment_listfields(dirList)
#segment_listfields(dirList2)
