# David Trethewey 31-07-2014
# use gdalmerge to create a layerstacked file
# with nadir image downsampled to DTM resolution
# and DTM and derived topographic layers
# output to same directory
# assume we are running from */mexhrs_2001/data directory
# under which each field is in directory XXXX
# assume filenames of form 'HXXXX_0000_da4.kea' etc.
import os.path
import sys
from rsgislib import imageutils
import rsgislib
from rsgislib import imagecalc
import glob
#import time
directory = os.getcwd()
print(directory)
dirList = os.listdir(directory)
dirList = [d for d in dirList if (os.path.isdir(d))]
print(dirList)
#dirList = ['1523', '1545', '5299', '2908', '5286', '5304', '1428', '1450','1461', '2224', '2279']
bandNames = ['Nadir image at DTM resolution', 'DTM areoid-elevation', 'Slope deg','Aspect deg from N', 'Cross-Sec Curvature','Longitudinal Curvature']


for f in dirList:
	os.chdir(f)
	os.chdir("LandSerf")
	listinputfiles_layerstack =  glob.glob('h'+f+'*LandSerfLayerstack3.kea')
	inputlayerstack = listinputfiles_layerstack[0]
	if len(listinputfiles_layerstack) > 1:
		print("More than one field in same directory")
		break 
	#outlayerstack_fname = inputlayerstack[:-4]+'_add9999.kea'
	outlayerstack_fname = inputlayerstack[:-5]+'_add9999_6band.kea'
# 1 = ND resampled to DTM res
# 2 = DTM
# 3 = slope
# 4 = aspectfromN
# 5 = CrsCrv
# 6 = LgtCrv
	#os.sys("rm -vf "+outlayerstack_fname)
	outFormat = 'KEA'
	dataType = rsgislib.TYPE_32FLOAT
	expression = 'b1+9999'
	imagecalc.imageMath(inputlayerstack, outlayerstack_fname, expression, outFormat, dataType)
	imageutils.setBandNames(outlayerstack_fname,bandNames)
	os.chdir("../..")
