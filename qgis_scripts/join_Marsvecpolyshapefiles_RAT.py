# This shapefile takes the intersected shapefile with context9
# Souness GLF footprints and joins it to the attributes from the csv file

from glob import glob
from os import path
import os
import processing

rootpath = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessCatalog3_backup/'
pathtoshp = 'LandSerf/rsgis_02sqkm'
os.chdir(rootpath)
dirList = os.listdir(rootpath)
dirList = [d for d in dirList if (os.path.isdir(d))]

for d in dirList:
    os.chdir(d)
    os.chdir(pathtoshp)
    currentdir = os.getcwd()
    vecshps = glob(path.join(currentdir,"*6band*vectorpolygons_isectCtx9.shp"))
    CSVts = glob(path.join(currentdir,"*6band*ASCII_RAT_GaussClass_noNDR.csv"))
    CSVt = CSVts[0]
    joinedshps = glob(path.join(currentdir,"*6band*vectorpolygons_joined.*"))
    for j in joinedshps:
        print("removing file {j}".format(j=j))
        os.system("rm -v {j}".format(j=j))
    for shp in vecshps:    
        (shpdir, shpfile) = path.split(shp)
        print("processing: {t}".format(t=shpfile))
        vecpolys = QgsVectorLayer(shp,shpfile,'ogr')               
        shpoutlayer = shpfile[:5] + "_joined"
        shpout = shp[:-4] + "_joined.shp"
        (_,shpoutfile) = path.split(shpout)
        p = processing.runalg('qgis:joinattributestable',vecpolys,CSVt,'DN','FID',None)
        joined = QgsVectorLayer(p['OUTPUT_LAYER'],shpoutfile,'ogr')
        e = QgsVectorFileWriter.writeAsVectorFormat(joined,shpoutfile,"CP1250",None,"ESRI Shapefile")
        if e == QgsVectorFileWriter.NoError:
            print("successfully wrote file {f}".format(f=shpoutfile))        
    os.chdir('../../..')
