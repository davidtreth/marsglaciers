# David Trethewey 30-08-2014

# assume we are running from */mexhrs_2001/data directory
# under which each field is in directory XXXX
# assume filenames of form 'HXXXX_0000_nd4.img' etc.
import os.path
import sys
import glob
#import time

#findDTMres_cmd = "gdalinfo *da4*img | grep 'Pixel Size' > DTMres.txt"

def calcAllStats(listDTMfields, extents, CTX, CTX9, points):
	outfileextentsbase = extents.split("/")[-1][:-4]+'_stats.csv'
	outfileCTXbase = CTX.split("/")[-1][:-4]+'_stats.csv'	
	outfileCTX9base = CTX9.split("/")[-1][:-4]+'_stats.csv'
	outfilepointsbase = points.split("/")[-1][:-4]+'_stats.csv'
	for f in listDTMfields:
		os.chdir(f)
                os.chdir("LandSerf")
		filename_layerstack = glob.glob("h*LandSerfLayerstack2.kea")[0]
		print(filename_layerstack)
#		os.system(findDTMres_cmd)
#                tresfile = open("DTMres.txt","r")
#		tres = tresfile.readlines()[0]
#        	tres = int(float(tres.split("(")[1].split(",")[0]))
#                tresfile.close()
#		filename_nd4 = 'h'+f+'_0000_nd4_Mars2000EqCyl_lat0_40.kea'
#		filename_nd4_resam = 'h'+f+'_0000_nd4_'+str(tres)+'_Mars2000EqCyl_lat0_40.kea'	
#		filename_da4 = 'h'+f+'_0000_da4_Mars2000EqCyl_lat0_40.kea'
		outstatsfile_layerstack_extents = 'h'+f+'_layerstack_'+outfileextentsbase
		outstatsfile_layerstack_CTX = 'h'+f+'_layerstack_'+outfileCTXbase
		outstatsfile_layerstack_CTX9 = 'h'+f+'_layerstack_'+outfileCTX9base
		outstatsfile_layerstack_points = 'h'+f+'_layerstack_'+outfilepointsbase
	
		zonalstats_cmdlayerstack_ext = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+extents+' --outstats '+ outstatsfile_layerstack_extents +' --min --max --mean --stddev --mode --minThreshold -9998 --force'
		zonalstats_cmdlayerstack_CTX = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+CTX+' --outstats '+ outstatsfile_layerstack_CTX +' --min --max --mean --stddev --mode --minThreshold -9998 --force'
		zonalstats_cmdlayerstack_CTX9 = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+CTX9+' --outstats '+ outstatsfile_layerstack_CTX9 +' --min --max --mean --stddev --mode --minThreshold -9998 --force'
		zonalstats_cmdlayerstack_points = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+heads+' --outstats '+ outstatsfile_layerstack_points +' --mean --mode --minThreshold -9998 --force'
		os.system(zonalstats_cmdlayerstack_ext)	
		os.system(zonalstats_cmdlayerstack_CTX)	
		os.system(zonalstats_cmdlayerstack_CTX9)	
		os.system(zonalstats_cmdlayerstack_points)	
		os.chdir("../..")

zonalstats_cmdbase = 'python ../../../../PythonScripts/rsgislib_zonalStats_DClewley.py'
extents_randomEqCyl = '../../../../SounessROIs/RandomExtents_HRSCtiles_Mars2000EqCyl_lat0_40.shp'
CTX_randomEqCyl = '../../../../SounessROIs/RandomContext_HRSCtiles_Mars2000EqCyl_lat0_40.shp'
CTX9_randomEqCyl = '../../../../SounessROIs/RandomContext9_HRSCtiles_all_Mars2000EqCyl_lat0_40.shp'
points_randomEqCyl = '../../../../SounessROIs/RandomPoints_HRSCtiles_Mars2000EqCyl_lat0_40.shp'



# subdirectory list list
# find all subdirectories in the current directory
directory = os.getcwd()
print(directory)
dirList = os.listdir(directory)
dirList = [d for d in dirList if (os.path.isdir(d))]
print(dirList)
calcAllStats(dirList, extents_randomEqCyl, CTX_randomEqCyl, CTX9_randomEqCyl, points_randomEqCyl)



