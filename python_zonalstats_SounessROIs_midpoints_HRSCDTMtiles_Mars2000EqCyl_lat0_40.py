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

def calcAllStats(listDTMfields, heads,m1,m2,m3,m4,mch,m6,m7,m8,m9,termini):
    # avoiding overwriting previous work by adding '_test' into filenames
    #outfileextentsbase = extents.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    #outfileCTXbase = CTX.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'	
    #outfileCTX9base = CTX9.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfileheadsbase = heads.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfilem1base = m1.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfilem2base = m2.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfilem3base = m3.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfilem4base = m4.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfilemchbase = mch.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfilem6base = m6.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfilem7base = m7.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfilem8base = m8.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfilem9base = m9.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    outfilemterminibase = termini.split("/")[-1][:-4]+'LandSerf3_stats_test.csv'
    
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
        #outstatsfile_layerstack_extents = 'h'+f+'_layerstack_'+outfileextentsbase
        #outstatsfile_layerstack_CTX = 'h'+f+'_layerstack_'+outfileCTXbase
        #outstatsfile_layerstack_CTX9 = 'h'+f+'_layerstack_'+outfileCTX9base
        outstatsfile_layerstack_heads = 'h'+f+'_layerstack_'+outfileheadsbase
        outstatsfile_layerstack_m1 = 'h'+f+_'layerstack_'+outfilem1base
        outstatsfile_layerstack_m2 = 'h'+f+_'layerstack_'+outfilem2base
        outstatsfile_layerstack_m3 = 'h'+f+_'layerstack_'+outfilem3base
        outstatsfile_layerstack_m4 = 'h'+f+_'layerstack_'+outfilem4base
        outstatsfile_layerstack_mch = 'h'+f+_'layerstack_'+outfilemchbase
        outstatsfile_layerstack_m6 = 'h'+f+_'layerstack_'+outfilem6base
        outstatsfile_layerstack_m7 = 'h'+f+_'layerstack_'+outfilem7base
        outstatsfile_layerstack_m8 = 'h'+f+_'layerstack_'+outfilem8base
        outstatsfile_layerstack_m9 = 'h'+f+_'layerstack_'+outfilem9base
        outstatsfile_layerstack_termini = 'h'+f+_'layerstack_'+outfileterminibase
    
        #zonalstats_cmdlayerstack_ext = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+extents+' --outstats '+ outstatsfile_layerstack_extents +' --min --max --mean --stddev --minThreshold -9998 --force'
        #zonalstats_cmdlayerstack_CTX = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+CTX+' --outstats '+ outstatsfile_layerstack_CTX +' --min --max --mean --stddev --minThreshold -9998 --force'
        #zonalstats_cmdlayerstack_CTX9 = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+CTX9+' --outstats '+ outstatsfile_layerstack_CTX9 +' --min --max --mean --stddev --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_heads = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+heads+' --outstats '+ outstatsfile_layerstack_heads +' --mean --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_m1 = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+m1+' --outstats '+ outstatsfile_layerstack_m1 +' --mean --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_m2 = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+m2+' --outstats '+ outstatsfile_layerstack_m2 +' --mean --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_m3 = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+m3+' --outstats '+ outstatsfile_layerstack_m3 +' --mean --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_m4 = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+m4+' --outstats '+ outstatsfile_layerstack_m4 +' --mean --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_mch = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+mch+' --outstats '+ outstatsfile_layerstack_mch +' --mean --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_m6 = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+m6+' --outstats '+ outstatsfile_layerstack_m6 +' --mean --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_m7 = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+m7+' --outstats '+ outstatsfile_layerstack_m7 +' --mean --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_m8 = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+m8+' --outstats '+ outstatsfile_layerstack_m8 +' --mean --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_m9 = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+m9+' --outstats '+ outstatsfile_layerstack_m9 +' --mean --minThreshold -9998 --force'
        zonalstats_cmdlayerstack_termini = zonalstats_cmdbase + ' --inimage '+ filename_layerstack + ' --invector '+termini+' --outstats '+ outstatsfile_layerstack_termini +' --mean --minThreshold -9998 --force'
        #os.system(zonalstats_cmdlayerstack_ext)	
        #os.system(zonalstats_cmdlayerstack_CTX)	
        #os.system(zonalstats_cmdlayerstack_CTX9)	
        os.system(zonalstats_cmdlayerstack_heads)
        os.system(zonalstats_cmdlayerstack_m1)
        os.system(zonalstats_cmdlayerstack_m2)
        os.system(zonalstats_cmdlayerstack_m3)
        os.system(zonalstats_cmdlayerstack_m4)
        os.system(zonalstats_cmdlayerstack_mch)
        os.system(zonalstats_cmdlayerstack_m6)
        os.system(zonalstats_cmdlayerstack_m7)
        os.system(zonalstats_cmdlayerstack_m8)
        os.system(zonalstats_cmdlayerstack_m9)
        os.system(zonalstats_cmdlayerstack_termini)	
        os.chdir("../..")

zonalstats_cmdbase = 'python /home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/rsgislib_zonalStats_DClewley.py'


#extents = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIextents_all_Mars2000EqCyl_lat0_40.shp'
#CTX = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIcontext_all_Mars2000EqCyl_lat0_40.shp'
#CTX9 = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIcontext9_all_Mars2000EqCyl_lat0_40.shp'
heads = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROIheads_all_Mars2000EqCyl_lat0_40.shp'
m1 = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROImidline1_all_Mars2000EqCyl_lat0_40.shp'
m2 = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROImidline2_all_Mars2000EqCyl_lat0_40.shp'
m3 = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROImidline3_all_Mars2000EqCyl_lat0_40.shp'
m4 = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROImidline4_all_Mars2000EqCyl_lat0_40.shp'
mch = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROImidchannel_all_Mars2000EqCyl_lat0_40.shp'
m6 = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROImidline6_all_Mars2000EqCyl_lat0_40.shp'
m7 = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROImidline7_all_Mars2000EqCyl_lat0_40.shp'
m8 = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROImidline8_all_Mars2000EqCyl_lat0_40.shp'
m9 = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROImidline9_all_Mars2000EqCyl_lat0_40.shp'
termini = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/SounessROItermini_all_Mars2000EqCyl_lat0_40.shp'

#extents_randomEqCyl = '../../../../SounessROIs/RandomExtents_HRSCtiles_Mars2000EqCyl_lat0_40.shp'
#CTX_randomEqCyl = '../../../../SounessROIs/RandomContext_HRSCtiles_Mars2000EqCyl_lat0_40.shp'
#CTX9_randomEqCyl = '../../../../SounessROIs/RandomContext9_HRSCtiles_all_Mars2000EqCyl_lat0_40.shp'
#points_randomEqCyl = '../../../../SounessROIs/RandomPoints_HRSCtiles_Mars2000EqCyl_lat0_40.shp'



# subdirectory list list
# find all subdirectories in the current directory
directory = os.getcwd()
print(directory)
dirList = os.listdir(directory)
dirList = [d for d in dirList if (os.path.isdir(d))]
print(dirList)
calcAllStats(dirList, heads,m1,m2,m3,m4,mch,m6,m7,m8,m9,termini)



