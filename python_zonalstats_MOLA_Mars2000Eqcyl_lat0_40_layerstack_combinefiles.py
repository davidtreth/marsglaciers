import csv
import os
import glob
import copy 

csvInFile = open('mmc1_Souness_Alldata.csv','r')

csv_reader = csv.reader(csvInFile)

outStatsFile = "SounessCatalog_MOLA_Mars2000EqCyl_lat0_40_combinedstats.csv"

#pathtodata = "SounessCatalog3/mexhrs_2001/data"
pathtodata = "MOLA_128"
os.chdir(pathtodata)

Headers_points = ["N","DTM_avg","DTM_mode","slope_avg","slope_mode","aspectN_avg","aspectN_mode","CrossScCrv_avg","CrossScCrv_mode","LongtCrv_avg","LongtCrv_mode","Feature_avg","Feature_mode","Npx"]
Headers_areas = ["N","DTM_min","DTM_max","DTM_avg","DTM_stddev","DTM_mode",
	"slope_min","slope_max","slope_avg","slope_stddev","slope_mode"
	"aspectN_min","aspectN_max","aspectN_avg","aspectN_stddev","aspectN_mode",
	"CrossScCrv_min","CrossScCrv_max","CrossScCrv_avg","CrossScCrv_stddev","CrossScCrv_mode",
	"LongtCrv_min","LongtCrv_max","LongtCrv_avg","LongtCrv_stddev","LongtCrv_mode",
	"LSrfFeat_min","LSrfFeat_max","LSrfFeat_avg","LSrfFeat_stddev","LSrfFeat_mode",
	"Npx"]
outRows = []

for row in enumerate(csv_reader):
	origrow = row[1]	
	if row[0]==0:
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
		print newrow
		outRows.append(newrow)
	else:				
		newrow = copy.copy(origrow)
		print newrow
		print "Row number %d" %	(row[0]-1)
#                searchstrN = "SounessROI*_N_stats.csv"
#                searchstrS = "SounessROI*_S_stats.csv"
                searchstr = "SounessROI*_*_stats.csv"
#                statsFileListN = sorted(glob.glob(searchstrN))
#                statsFileListS = sorted(glob.glob(searchstrS))
                statsFileList = sorted(glob.glob(searchstr))
                for s in statsFileList:
                        header_prefix = s.split("SounessROI")[1].split("_")[0]
                        statsInFile = open(s,'r')
                        csv_reader_stats = csv.reader(statsInFile)
                        for srow in csv_reader_stats:
                                if not(srow[0] =="FID"):						
                                        if int(srow[0])+1 == row[0]:
                                                print newrow, srow
                                                newrow.extend(srow)
                        statsInFile.close()
			print(newrow)
			outRows.append(newrow)

with open(outStatsFile, 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for r in outRows:
	    spamwriter.writerow(r)
