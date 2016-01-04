import glob
import os
import csv
import sys 
import pyproj
#main
#catalogInFile = open(sys.argv[1],"r")
catalogInFile = open("mmc1_HRSC+HiRISE_coverage_forsummarystats_cleaned.csv","r")

catalogOutFile_alldata = "mmc1_Souness_Alldata.csv"

catalogOutF_All = open(catalogOutFile_alldata ,"w")


catalogOutFile_ColHeadings = ['Catalogue number', 'Parent image ID',
                              'Mars Express/HRSC DTM (best resolution)', 'HRSC DTM resolution (m/px)',
                              'HiRISE available?','HiRISE image','HiRISE anaglyph','HiRISE DTM',
                              'GLF Head lon. (+/- 180)','GLF Head lat.',
                              'GLF Terminus lon. (+/- 180)', 'GLF Terminus lat.',
                              'Mid-channel true right lon. (+/- 180)', 'Mid-channel true right lat.',
                              'Mid-channel true left lon. (+/- 180)','Mid-channel true left lat.',
                              'Centre lon. (+/- 180)', 'Centre lat.',
                              'GLF length (km)', 'GLF width (km)', 'GLF area (km sq.)',
                              'GLF orientation (deg.)',
                              'Buffer min elevation (m)','Buffer max elevation (m)',
                              'Buffer Mean elevation (m)', 'Buffer Std. Dev. elevation (m)',
                              'Elongation','TM central longitude',
                              'Head X', 'Head Y', 'Terminus X','Terminus Y',
                              'Mid-channelR X','Mid-channelR Y','Mid-channelL X','Mid-channelL Y',
                              'Centre X', 'Centre Y']

p1 = pyproj.Proj('+proj=longlat +a=3396190 +b=3376200 +no_defs')
p2 = pyproj.Proj('+proj=eqc +lat_ts=40 +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +a=3396190 +b=3376200 +units=m +no_defs')

#Leftovers from a previous plan to use several different coordinate bases for different subregions
#p2D = pyproj.Proj('+proj=tmerc +lat_0=0 +lon_0=25 +k=0.9996 +x_0=0 +y_0=0 +a=3396190 +b=3376200 +units=m +no_defs')
#p2P = pyproj.Proj('+proj=tmerc +lat_0=0 +lon_0=60 +k=0.9996 +x_0=0 +y_0=0 +a=3396190 +b=3376200 +units=m +no_defs')
#p2M = pyproj.Proj('+proj=tmerc +lat_0=0 +lon_0=-80 +k=0.9996 +x_0=0 +y_0=0 +a=3396190 +b=3376200 +units=m +no_defs')
#p2R = pyproj.Proj('+proj=tmerc +lat_0=0 +lon_0=105 +k=0.9996 +x_0=0 +y_0=0 +a=3396190 +b=3376200 +units=m +no_defs')

         
csv_reader = csv.reader(catalogInFile)
for row in enumerate(csv_reader):
        if row[0] == 0:
                outputStrHeader = "HeadX"+","+"HeadY"+","+"CentreX"+","+"CentreY"+","+"TerminiX"+","+"TerminiY"+","+"LeftMidChX"+","+"LeftMidChY"+","+"RightMidChX"+","+"RightMidChY"+","+"Length_km"+","+"Width_km"+","+"Area_kmsq"+","+"Orientation"+","+"CatNumber"+","+"CentreLong"+","+"CentreLat"+","+"DTMtile"+","+"DTMres"+","+"HiRISE"+","+"HiRISEANAGLYPH"+","+"HiRISEDTM"+"\n"
                #Leftovers from a previous plan to use several different coordinate bases for different subregions
#                catalogOutF_P.write(outputStrHeader)
#                catalogOutF_D.write(outputStrHeader)
#                catalogOutF_M.write(outputStrHeader)
#                catalogOutF_R.write(outputStrHeader)
                catalogOutF_All.write(outputStrHeader)
                continue
        else:
                # get locations of head, centre, terminus
                # and left/right of channel from input
                Hlat = float(row[1][10])
                Hlng = float(row[1][9])
                Clat = float(row[1][22])
                Clng = float(row[1][21])
                Tlat = float(row[1][13])
                Tlng = float(row[1][12])
                LClat = float(row[1][19])
                LClng = float(row[1][18])
                RClat = float(row[1][16])
                RClng = float(row[1][15])
                # use pyproj to transform to the new basis
                x1H, y1H = p1(Hlng, Hlat)
                print Hlng, Hlat, x1H, y1H
                x2H, y2H = pyproj.transform(p1, p2,x1H, y1H,radians=True)
                x1C, y1C = p1(Clng, Clat)
                x2C, y2C = pyproj.transform(p1, p2,x1C,y1C,radians=True)
                x1T, y1T = p1(Tlng, Tlat)
                x2T, y2T = pyproj.transform(p1, p2,x1T,y1T,radians=True)
                x1LC, y1LC = p1(LClng, LClat)
                x2LC, y2LC = pyproj.transform(p1, p2,x1LC,y1LC,radians=True)
                x1RC, y1RC = p1(RClng, RClat)
                x2RC, y2RC = pyproj.transform(p1, p2,x1RC,y1RC,radians=True)

                DTMfn = '"'+row[1][2]+'"'
                DTMres = row[1][3] #could be a number except for some fields that are not numbers
                HiRISEfn = '"'+row[1][5]+'"'
                HiRISE3Dfn = '"'+row[1][6]+'"'
                HiRISEDTMfn = '"'+row[1][7]+'"'

                outputStr_AllD = str(x2H)+','+str(y2H)+','+str(x2C)+','+str(y2C)+','+str(x2T)+','+str(y2T)+','+str(x2LC)+','+str(y2LC)+','+str(x2RC)+','+str(y2RC)+','+row[1][23]+','+row[1][24]+','+row[1][25]+','+row[1][26]+','+row[1][0]+','+row[1][21]+','+row[1][22]+','+DTMfn+','+DTMres+','+HiRISEfn+','+HiRISE3Dfn+','+HiRISEDTMfn+'\n'            

                #outputStr_AllDR_ll = row[1][9]+','+row[1][10]+','+row[1][21]+','+row[1][22]+','+row[1][12]+','+row[1][13]+','+row[1][18]+','+row[1][19]+','+row[1][15]+','+row[1][16]+','+row[1][23]+','+row[1][24]+','+row[1][25]+','+row[1][26]+','+row[1][0]+','+DTMfn+','+DTMres+','+HiRISEfn+','+HiRISE3Dfn+','+HiRISEDTMfn+'\n'
     
                catalogOutF_All.write(outputStr_AllD)
#                catalogOutF_Rll.write(outputStr_AllDR_ll)
catalogInFile.close()     
catalogOutF_All.close()
#catalogOutF_P.close()
#catalogOutF_D.close()
#catalogOutF_M.close()
#catalogOutF_R.close()

#catalogOutF_Pll.close()
#catalogOutF_Dll.close()
#catalogOutF_Mll.close()
#catalogOutF_Rll.close()

