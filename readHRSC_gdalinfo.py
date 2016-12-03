# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 11:52:16 2016

@author: David Trethewey

This program will eventually consolidate information from the 

DA4, ND4 and layerstack gdalinfo
and combine with information about the Souness objects
and output to a single json file
"""

import subprocess
import json
import os.path
import glob
from matplotlib import pyplot as plt

Souness_HRSC_pathroot =  '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessCatalog3_backup/'

os.chdir(Souness_HRSC_pathroot)

dirList = os.listdir(Souness_HRSC_pathroot)
dirList = [d for d in dirList if (os.path.isdir(d))]
dirList.sort()

try:
    intdirs = [int(i) for i in dirList]
except:
    print("all directories under this folder should be {nnnn} for each HRSC tile.")

# DA4 elevation tile
HRSCdict = {}
# ND4 nadir image tile
HRSC_nd4dict = {}
# layerstack in equicylindrical projection
HRSC_Lyr2dict = {}
for d in dirList:
    os.chdir(d)
    da4 = glob.glob("h*da4.img")
    # make sure each directory contains 1 *da4.img file
    assert(len(da4) ==1)
    #print(da4)
    gdalinf = subprocess.check_output("gdalinfo -json {f}".format(f=da4[0]), shell=True)
    gdaljson_da4 = json.loads(gdalinf)
    #print(gdaljson_da4)
    tileID = gdaljson_da4['description'][:5]
    print("reading tile {t}".format(t=tileID))
    HRSCdict[tileID] = gdaljson_da4
    
    # the reprojected nadir image
    # to the Mars equicylindrical system centred at 40 deg
    nd4 = glob.glob("h*nd4*Mars2000EqCyl_lat0_40.kea")        
    assert(len(nd4) ==1)
    gdalinf = subprocess.check_output("gdalinfo -json {f}".format(f=nd4[0]), shell=True)
    gdaljson_nd4 = json.loads(gdalinf)
    #print(gdaljson_nd4)
    tileID = gdaljson_nd4['description'][:5]
    HRSC_nd4dict[tileID] = gdaljson_nd4
    
    os.chdir("LandSerf")
    # the 10 band layerstack with nadir, dtm, derived topographic values
    Layerstack2 = glob.glob("h*LandSerfLayerstack2.kea")
    # expect 1 of these files
    assert(len(Layerstack2)==1)
    gdalinf = subprocess.check_output("gdalinfo -json {f}".format(f=Layerstack2[0]), shell=True)
    gdaljson_Lyr2 = json.loads(gdalinf)
    #print(gdaljson_Lyr2)
    tileID = gdaljson_Lyr2['description'][:5]
    HRSC_Lyr2dict[tileID] = gdaljson_Lyr2
    
    os.chdir("../..")
    
    
tilenames = HRSCdict.keys()
HRSCdata = HRSCdict.values()

latlng_coords =  [v['wgs84Extent']['coordinates'][0] for v in HRSCdata]
upperLefts = [c[0] for c in latlng_coords]
upperRights = [c[2] for c in latlng_coords]
lowerLefts = [c[1] for c in latlng_coords]
lowerRights = [c[3] for c in latlng_coords]
polygons = zip(upperLefts, upperRights, lowerRights, lowerLefts, upperLefts)

geotransf = [v['geoTransform'] for v in HRSCdata]
res = [g[1] for g in geotransf]
""" using original coordinates Mars sinusoidal
this got somewhat confusing
# cornercoords = [v['cornerCoordinates'] for v in HRSCdata]
# upperRights = [c['upperRight'] for c in cornercoords]
# upperLefts = [c['upperLeft'] for c in cornercoords]
# lowerLefts = [c['lowerLeft'] for c in cornercoords]
# lowerRights = [c['lowerRight'] for c in cornercoords]
# polygons = [[z[0], z[1], z[2], z[3], z[0]] for z in zip(upperLefts, upperRights, lowerRights, lowerLefts)]
# x_offs = [g[0] for g in geotransf]
# y_offs = [g[3] for g in geotransf]
"""

for tn, p, r in zip(tilenames, polygons, res):
    print("tile: {t} polygon: {pl} resolution: {r}m".format(t=tn, pl=p,r=r))
    x = [i[0]  for i in p]
    y = [i[1]  for i in p]    
    print(x,y)
    plt.plot(x,y, "k-")
    plt.title("179 HRSC DTM tiles")
    plt.xlim([-180,180])
plt.show()