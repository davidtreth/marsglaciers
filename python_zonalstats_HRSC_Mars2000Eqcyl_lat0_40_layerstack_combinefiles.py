# David Trethewey
# work in progress 04-01-2016
# to reconstuct script for collating zonalstats data

import csv
import os
import glob
import copy 

csvInFile = open('mmc1_Souness_Alldata.csv','r')

csv_reader = csv.reader(csvInFile)

#outStatsFile = "SounessCatalog_MOLA_Mars2000EqCyl_lat0_40_combinedstats.csv"
outStatsFile = "SounessCatalog_Mars2000EqCyl_lat0_40_combinedstats_allLandSerf3.csv"
#outStatsFile = "testoutstats.csv"

#pathtodata = "SounessCatalog3/mexhrs_2001/data"
#pathtodata = "MOLA_128"
pathtodata = "/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessCatalog3_backup"
# just so we don't overwrite the original
outstatspath = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers'


Headers_points = ["N","NDR_avg","DTM_avg","slope_avg","aspectN_avg","CrossScCrv_avg","LongtCrv_avg","Npx"]
Headers_areas = ["N","NDR_min","NDR_max","NDR_avg","NDR_stddev",
                 "DTM_min","DTM_max","DTM_avg","DTM_stddev",
	"slope_min","slope_max","slope_avg","slope_stddev",
	"aspectN_min","aspectN_max","aspectN_avg","aspectN_stddev",
	"CrossScCrv_min","CrossScCrv_max","CrossScCrv_avg","CrossScCrv_stddev",
	"LongtCrv_min","LongtCrv_max","LongtCrv_avg","LongtCrv_stddev",
	"Npx"]
outRows = []

os.chdir(pathtodata)
for row in enumerate(csv_reader):
    # iterate through mmc1_Souness_Alldata.csv
    # that is, the Souness catalogue
    # with locations transformed to Mars eqcyl 40
    origrow = row[1]
    print(origrow)
    if row[0] == 0:
        # extend the headers in the first row
        newrow = copy.copy(origrow)
        centres = ["centres_"+h for h in Headers_points]
        context9 = ["context9_"+h for h in Headers_areas]
        context = ["context_"+h for h in Headers_areas]
        extents = ["extent_"+h for h in Headers_areas]
        heads5km = ["heads5km_"+h for h in Headers_areas]
        heads = ["heads_"+h for h in Headers_points]
        termini = ["termini_"+h for h in Headers_points]
        newrow.extend(centres)
        newrow.extend(context9)
        newrow.extend(context)
        newrow.extend(extents)
        newrow.extend(heads5km)
        newrow.extend(heads)
        newrow.extend(termini)
        print(newrow)
        outRows.append(newrow)
    else:
        # start with the row from csvInFile
        newrow = copy.copy(origrow)
        # find which DTM tile is given
        # if any in the csvInFile
        if newrow[17][0:4].lower() == 'none':
            continue
        dirField = str(newrow[17][1:5])
        print dirField
        os.chdir(dirField)
        os.chdir("LandSerf")
        print "Row number %d" %	(row[0]-1)
        #searchstrN = "SounessROI*_N_stats.csv"
        #searchstrS = "SounessROI*_S_stats.csv"
        searchstr = "h*layerstack_SounessROI*_LandSerf3_stats.csv"
        #statsFileListN = sorted(glob.glob(searchstrN))
        #statsFileListS = sorted(glob.glob(searchstrS))
        statsFileList = sorted(glob.glob(searchstr))
        print("statsfiles = {s}".format(s=statsFileList))
        for s in statsFileList:
            header_prefix = s.split("SounessROI")[1].split("_")[0]
            statsInFile = open(s,'r')
            csv_reader_stats = csv.reader(statsInFile)
            for srow in csv_reader_stats:
                if not(srow[0] =="FID"):
                    # make sure this isn't the first row
                    # that contains the headers
                    if int(srow[0])+1 == row[0]:
                        # if this is the same GLF as in index
                        # from the csvInfile                        
                        print newrow, srow
                        newrow.extend(srow)
        statsInFile.close()
        print(newrow)
        outRows.append(newrow)
        os.chdir("../..")

os.chdir(outstatspath)
with open(outStatsFile, 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for r in outRows:
	    spamwriter.writerow(r)


directory = os.getcwd()
print(directory)
dirList = os.listdir(directory)
dirList = [d for d in dirList if (os.path.isdir(d))]
print(dirList)
