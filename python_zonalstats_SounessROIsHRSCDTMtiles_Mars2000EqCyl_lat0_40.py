# David Trethewey 04-01-2016

# this is untested code that is liable to not work

# assume we are running from */mexhrs_2001/data directory
# under which each field is in directory XXXX
# assume filenames of form 'HXXXX_0000_nd4.img' etc.
import os.path
import sys
import glob
#import time

#findDTMres_cmd = "gdalinfo *da4*img | grep 'Pixel Size' > DTMres.txt"

def calcAllStats(listDTMfields, extents, CTX, CTX9, heads):
    # avoiding overwriting previous work by adding '_test' into filenames
    outfileextentsbase = extents.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfileCTXbase = CTX.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'	
    outfileCTX9base = CTX9.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfileheadsbase = heads.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    for f in listDTMfields:
        os.chdir(f)
        os.chdir("LandSerf")
        filename_layerstack = glob.glob("h*LandSerfLayerstack3.kea")[0]
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
        outstatsfile_layerstack_heads = 'h'+f+'_layerstack_'+outfileheadsbase	
        zonalstats_cmdlayerstack_ext = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+extents+' --outstats '+ outstatsfile_layerstack_extents +' --min --max --mean --stddev --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_CTX = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+CTX+' --outstats '+ outstatsfile_layerstack_CTX +' --min --max --mean --stddev --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_CTX9 = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+CTX9+' --outstats '+ outstatsfile_layerstack_CTX9 +' --min --max --mean --stddev --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_heads = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+heads+' --outstats '+ outstatsfile_layerstack_heads +' --mean --minThreshold -9998 --force'
        os.system(zonalstats_cmdlayerstack_ext)	
        os.system(zonalstats_cmdlayerstack_CTX)	
        os.system(zonalstats_cmdlayerstack_CTX9)	
        os.system(zonalstats_cmdlayerstack_heads)	
        os.chdir("../..")

zonalstats_cmdbase = 'python /home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/rsgislib_zonalStats_DClewley.py'

extents = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROIextents_all_Mars2000EqCyl_lat0_40.shp'
CTX = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROIcontext_all_Mars2000EqCyl_lat0_40.shp'
CTX9 = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROIcontext9_all_Mars2000EqCyl_lat0_40.shp'
heads = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROIheads_all_Mars2000EqCyl_lat0_40.shp'

#extents_randomEqCyl = '../../../../SounessROIs/RandomExtents_HRSCtiles_Mars2000EqCyl_lat0_40.shp'
#CTX_randomEqCyl = '../../../../SounessROIs/RandomContext_HRSCtiles_Mars2000EqCyl_lat0_40.shp'
#CTX9_randomEqCyl = '../../../../SounessROIs/RandomContext9_HRSCtiles_all_Mars2000EqCyl_lat0_40.shp'
#points_randomEqCyl = '../../../../SounessROIs/RandomPoints_HRSCtiles_Mars2000EqCyl_lat0_40.shp'



# subdirectory list list
# find all subdirectories in the current directory
directory = os.getcwd()
print(directory)
#dirList = os.listdir(directory)
#dirList = [d for d in dirList if (os.path.isdir(d))]
dirList = ["5231"]
print(dirList)
calcAllStats(dirList, extents, CTX, CTX9, heads)



