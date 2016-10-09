# This script takes the shapefiles which are the result of segmenting the DEM layerstack
# with RSGISlib and intersects them with the Souness GLF head, 5km around head, extent
# context, and context9 shapefiles and outputs these to the same directory of each HRSC field.

from glob import glob
from os import path
import os
import processing

rootpath = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessCatalog3_backup/'
Souness_extshp = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessROIs/SounessROIextents_all_Mars2000EqCyl_lat0_40.shp'
Souness_headshp = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessROIs/SounessROIheads_all_Mars2000EqCyl_lat0_40.shp'
Souness_head5kmshp = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessROIs/SounessROIheads_5km_all_Mars2000EqCyl_lat0_40.shp'
Souness_ctxshp = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessROIs/SounessROIcontext_all_Mars2000EqCyl_lat0_40.shp'
Souness_ctx9shp = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessROIs/SounessROIcontext9_all_Mars2000EqCyl_lat0_40.shp'

pathtoshp = 'LandSerf/rsgis_02sqkm'
#MarsEqCyl40 = QgsCoordinateReferenceSystem()
#MarsEqCyl40.createFromProj4("+proj=eqc +lat_ts=40 +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +a=3396190 +b=3376200 +units=m +no_defs")

os.chdir(rootpath)
dirList = os.listdir(rootpath)
dirList = [d for d in dirList if (os.path.isdir(d))]
SouExts = QgsVectorLayer(Souness_extshp,'SounessExts','ogr')
SouHeads = QgsVectorLayer(Souness_headshp,'SounessHeads','ogr')
SouHead5kms = QgsVectorLayer(Souness_head5kmshp,'SounessHead5kms','ogr')
SouCtxs = QgsVectorLayer(Souness_ctxshp,'SounessCtxs','ogr')
SouCtx9s = QgsVectorLayer(Souness_ctx9shp,'SounessCtx9s','ogr')

#dirList0 = ['0022']
#iface.addVectorLayer(shp,shpfile,'ogr')
#isect = iface.addVectorLayer(p['OUTPUT'],shpoutfile,'ogr')
for d in dirList:
    os.chdir(d)
    os.chdir(pathtoshp)
    currentdir = os.getcwd()
    #isectoutput = glob(path.join(currentdir,"*vectorpolygons_isectExt.*"))
    #print("removing existing isect files")
    #for isect in isectoutput:        
    #    os.system("rm -v {i}".format(i=isect))
    vecshps = glob(path.join(currentdir,"*6band*vectorpolygons.shp"))
    for shp in vecshps:    
        (shpdir, shpfile) = path.split(shp)
        print("processing: {t}".format(t=shpfile))
        vecpolys = QgsVectorLayer(shp,shpfile,'ogr')        
    #    shpoutlayer = shpfile[:5] + "_isectExt"
    #    shpout = shp[:-4] + "_isectExt.shp"
    #    (_,shpoutfile) = path.split(shpout)
    #    p = processing.runalg('qgis:extractbylocation',vecpolys,SouExts,['intersects'],None)
    #    isect = QgsVectorLayer(p['OUTPUT'],shpoutfile,'ogr')
    #    e = QgsVectorFileWriter.writeAsVectorFormat(isect,shpoutfile,"utf-8",None,"ESRI Shapefile")
    #    if e == QgsVectorFileWriter.NoError:
    #        print("successfully wrote file {f}".format(f=shpoutfile))
        shpoutlayer = shpfile[:5] + "_isectHead"
        shpout = shp[:-4] + "_isectHead.shp"
        (_,shpoutfile) = path.split(shpout)
        p = processing.runalg('qgis:extractbylocation',vecpolys,SouHeads,['intersects'],None)
        isect = QgsVectorLayer(p['OUTPUT'],shpoutfile,'ogr')
        e = QgsVectorFileWriter.writeAsVectorFormat(isect,shpoutfile,"utf-8",None,"ESRI Shapefile")
        if e == QgsVectorFileWriter.NoError:
            print("successfully wrote file {f}".format(f=shpoutfile))
            
        shpoutlayer = shpfile[:5] + "_isectHead5km"
        shpout = shp[:-4] + "_isectHead5km.shp"
        (shpoutdir,shpoutfile) = path.split(shpout)
        p = processing.runalg('qgis:extractbylocation',vecpolys,SouHead5kms,['intersects'],None)
        isect = QgsVectorLayer(p['OUTPUT'],shpoutfile,'ogr')
        e = QgsVectorFileWriter.writeAsVectorFormat(isect,shpoutfile,"utf-8",None,"ESRI Shapefile")
        if e == QgsVectorFileWriter.NoError:
            print("successfully wrote file {f}".format(f=shpoutfile))
            
        shpoutlayer = shpfile[:5] + "_isectCtx"
        shpout = shp[:-4] + "_isectCtx.shp"
        (shpoutdir,shpoutfile) = path.split(shpout)
        p = processing.runalg('qgis:extractbylocation',vecpolys,SouCtxs,['intersects'],None)
        isect = QgsVectorLayer(p['OUTPUT'],shpoutfile,'ogr')
        e = QgsVectorFileWriter.writeAsVectorFormat(isect,shpoutfile,"utf-8",None,"ESRI Shapefile")
        if e == QgsVectorFileWriter.NoError:
            print("successfully wrote file {f}".format(f=shpoutfile))
            
        shpoutlayer = shpfile[:5] + "_isectCtx9"
        shpout = shp[:-4] + "_isectCtx9.shp"
        (shpoutdir,shpoutfile) = path.split(shpout)
        p = processing.runalg('qgis:extractbylocation',vecpolys,SouCtx9s,['intersects'],None)
        isect = QgsVectorLayer(p['OUTPUT'],shpoutfile,'ogr')
        e = QgsVectorFileWriter.writeAsVectorFormat(isect,shpoutfile,"utf-8",None,"ESRI Shapefile")
        if e == QgsVectorFileWriter.NoError:
            print("successfully wrote file {f}".format(f=shpoutfile))
        
    os.chdir('../../..')
