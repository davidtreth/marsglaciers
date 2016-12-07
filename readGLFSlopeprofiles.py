import csv
import os
import subprocess
import glob
import matplotlib.pyplot as plt
import numpy

dataPath = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessCatalog3_backup'
outPath = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/ProfilePNGs/'
globq = "*Layerstack_rawAsp.kea"

csvInFile = 'SounessGLFprofiles.csv'



with open(csvInFile,"r") as csvfile:
    spamreader = csv.reader(csvfile,delimiter=',',quotechar='"')
    for row in spamreader:
        print("Catalogue number {n}, HRSC tile {h}.".format(n=row[0],h=row[1]))
        #print("Midpoint line coordinates {L}\n".format(L = row[2:]))
        if row[1][1:5] == 'none':
            continue
        else:
            HRSCtile = row[1][2:6]
            outFile = outPath + row[0]+"_"+row[1][1:6]+".txt"
            outPNG = outPath + "SounessCat{n:04d}_{h}_Slope.png".format(n=int(row[0]),h=row[1][1:6])
            os.chdir(dataPath)
            os.chdir(HRSCtile)
            os.chdir('LandSerf')
            KEAfile = glob.glob(globq)[0]
            gdalcmd0 = "gdallocationinfo -valonly -b 3 -geoloc {f} {x} {y}".format(f=KEAfile,x=float(row[2]),y=float(row[3]))
            gdalcmd1 = "gdallocationinfo -valonly -b 3 -geoloc {f} {x} {y}".format(f=KEAfile,x=float(row[5]),y=float(row[6]))
            gdalcmd2 = "gdallocationinfo -valonly -b 3 -geoloc {f} {x} {y}".format(f=KEAfile,x=float(row[8]),y=float(row[9]))
            gdalcmd3 = "gdallocationinfo -valonly -b 3 -geoloc {f} {x} {y}".format(f=KEAfile,x=float(row[11]),y=float(row[12]))
            gdalcmd4 = "gdallocationinfo -valonly -b 3 -geoloc {f} {x} {y}".format(f=KEAfile,x=float(row[14]),y=float(row[15]))
            gdalcmd5 = "gdallocationinfo -valonly -b 3 -geoloc {f} {x} {y}".format(f=KEAfile,x=float(row[17]),y=float(row[18]))
            gdalcmd6 = "gdallocationinfo -valonly -b 3 -geoloc {f} {x} {y}".format(f=KEAfile,x=float(row[20]),y=float(row[21]))
            gdalcmd7 = "gdallocationinfo -valonly -b 3 -geoloc {f} {x} {y}".format(f=KEAfile,x=float(row[23]),y=float(row[24]))
            gdalcmd8 = "gdallocationinfo -valonly -b 3 -geoloc {f} {x} {y}".format(f=KEAfile,x=float(row[26]),y=float(row[27]))
            gdalcmd9 = "gdallocationinfo -valonly -b 3 -geoloc {f} {x} {y}".format(f=KEAfile,x=float(row[29]),y=float(row[30]))
            gdalcmd10 = "gdallocationinfo -valonly -b 3 -geoloc {f} {x} {y}".format(f=KEAfile,x=float(row[32]),y=float(row[33]))
            #os.system("rm "+outFile)
            h = subprocess.check_output(gdalcmd0,shell=True)
            #print("head elev {h}".format(h=h))
            m1 = subprocess.check_output(gdalcmd1,shell=True) 
            m2 = subprocess.check_output(gdalcmd2,shell=True) 
            m3 = subprocess.check_output(gdalcmd3,shell=True) 
            m4 = subprocess.check_output(gdalcmd4,shell=True) 
            m5 = subprocess.check_output(gdalcmd5,shell=True) 
            m6 = subprocess.check_output(gdalcmd6,shell=True) 
            m7 = subprocess.check_output(gdalcmd7,shell=True) 
            m8 = subprocess.check_output(gdalcmd8,shell=True) 
            m9 = subprocess.check_output(gdalcmd9,shell=True) 
            t = subprocess.check_output(gdalcmd10,shell=True)
            rvect = [float(row[4]),float(row[7]),float(row[10]),float(row[13]),float(row[16]),float(row[19]),float(row[22]),float(row[25]),
                     float(row[28]),float(row[31]),float(row[34])]
            slopevect = [h,m1,m2,m3,m4,m5,m6,m7,m8,m9,t]
            print(slopevect)
            if h == '\n' or t == '\n':
                continue
            else:
                slopevect = [float(z[:-1]) for z in slopevect]
                #print(elevvect)
                minslope = float(numpy.min(slopevect))
                maxslope = float(numpy.max(slopevect))
                if minslope > -9999:
                    plt.figure()
                    plt.plot(rvect,slopevect)
                    plt.title("Slope profile Souness {n:04d}, HRSC tile h{tnum}".format(n=int(row[0]), tnum=HRSCtile))
                    plt.xlabel("Distance along midline (m)")
                    plt.ylabel("Slope (degrees)")
                    plt.savefig(outPNG)
        os.chdir("../..")
                    


#outPNG = outPath+"allGLFSlopeprof.png"
#plt.savefig(outPNG)
