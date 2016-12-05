# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 11:52:16 2016

@author: David Trethewey

This program will eventually consolidate information from the 

DA4, ND4 and layerstack gdalinfo
and combine with information about the Souness objects
and output to a single json file

It will also compare the list of HRSC tiles with the one from intersecting
the HRSC DTM footprints with Souness extents
"""

import subprocess
import json
import os.path
import glob
from matplotlib import pyplot as plt

def printgdaljson(gdaljson):
    for i in gdaljson:
        if i == 'rat':
            pass
        elif i == 'bands':
            print("bands:\n    Number of bands = {nb}".format(nb=len(gdaljson[i])))
            for b in gdaljson[i]:
                print("\n    Band {n}:".format(n=b['band']))
                for j in b:
                    print("        {j}: {v}".format(j=j, v=b[j]))
        else:
            print("{i}: {v}".format(i=i,v=gdaljson[i]))


def readTileGDAL(tileglobstr, label, verbose=False):
    files = glob.glob(tileglobstr)
    # expect one of each da4 file, and nd4 file in the directory
    assert(len(files)==1)
    gdalinf = subprocess.check_output("gdalinfo -json {f}".format(f=files[0]), shell=True)
    gdaljson = json.loads(gdalinf)
    tileID = gdaljson['description'][:5]
    print("tileID = {t}".format(t=tileID))
    print("\n{l} file {d}".format(l=label, d=files[0]))
    if verbose:
        print(gdaljson)
    return gdaljson, tileID
                 
def readfromHRSCfiles(HRSC_pathroot):
    os.chdir(HRSC_pathroot)
    dirList = os.listdir(HRSC_pathroot)
    dirList = [d for d in dirList if (os.path.isdir(d))]
    dirList.sort()

    try:
        intdirs = [int(i) for i in dirList]
    except:
        print("all directories under this folder should be {nnnn} for each HRSC tile.")

    # DA4 elevation tile
    HRSC_da4dict = {}
    # ND4 nadir image tile
    HRSC_nd4dict = {}
    # layerstack in equicylindrical projection
    HRSC_Lyr2dict = {}
    for d in dirList:
        os.chdir(d)
        print("\nReading directory {d}".format(d=d))
        # the da4 areoid digital terrain model
        da4json, tileID = readTileGDAL("h*da4.img", "da4")
        HRSC_da4dict[tileID] = da4json
        # the reprojected nadir image
        # to the Mars equicylindrical system centred at 40 deg
        nd4json, tileID = readTileGDAL("h*nd4*Mars2000EqCyl_lat0_40.kea", "nd4")
        HRSC_nd4dict[tileID] = nd4json
        os.chdir("LandSerf")
        # the 10 band layerstack with nadir, dtm, derived topographic values
        lyrsjson, tileID = readTileGDAL("h*LandSerfLayerstack2.kea", "layerstack file")
        HRSC_Lyr2dict[tileID] = lyrsjson
        
        os.chdir("../..")
    return HRSC_da4dict, HRSC_nd4dict, HRSC_Lyr2dict



currentdir = os.getcwd()    
HRSC_pathroot =  '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessCatalog3_backup/'
HRSC_da4dict, HRSC_nd4dict, HRSC_Lyr2dict = readfromHRSCfiles(HRSC_pathroot)
os.chdir(currentdir)

#print(tilenames)



isect_DTMresJSON = "SounessROIs/HRSC_DTMres_index_extent.json"
isect_DTMSounesslistJSON = "SounessROIs/HRSCdtm_tiles_isect_extent_sounessobjs.json"
souness_DTMtiles = "SounessROIs/souness_extent_HRSCdtm_tiles.json"
souness_GLFsJSON = "souness_glf.json"

with open(isect_DTMresJSON) as jsonfile:
    DTMres = json.load(jsonfile)
with open(isect_DTMSounesslistJSON) as jsonfile:
    HRSC_Souness = json.load(jsonfile)
with open(souness_DTMtiles) as jsonfile:
    souness_DTMs = json.load(jsonfile)
with open(souness_GLFsJSON) as jsonfile:
    sounessGLFs = json.load(jsonfile)
    sounessGLFs = sounessGLFs["Souness"]
    
#print(DTMres)
def print_tiles_notused(DTMres, HRSC_DA4_GDALdict, quiet=True):
    tilenames = HRSC_DA4_GDALdict
    for t in DTMres:
        if t.lower() not in tilenames:
            sounessobjs = HRSC_Souness[t]
            dtm_res = DTMres[t]['resolution']
            notfound = "none"
            minres = 0
            
            for s in sounessobjs:
                if "HRSC_DTM_res" in sounessGLFs[str(s)]:
                    notfound = ""
                    if float(sounessGLFs[str(s)]["HRSC_DTM_res"]) > minres:
                        minres = float(sounessGLFs[str(s)]["HRSC_DTM_res"])
                else:
                    minres = 500
                        
            #print(dtm_res, minres)
            bestresused = (dtm_res >= minres) 
            print("Tile {t}: Resolution {r}m.\nProduct ID: {p}. URL: {b}\nSouness objects: {s}".format(t=t,
                                                                                                         r=DTMres[t]['resolution'],
                                                                                                         p=DTMres[t]['prodID'],
                                                                                                         b=DTMres[t]['url'],
                                                                                                         s=sounessobjs))
            if bestresused:
                print("Best available resolution used for all Souness objects in this tile")
            if not(bestresused and quiet):
                print("In dissertation, following HRSC DTM tiles used:")
                for s in sounessobjs:
                    tileused = sounessGLFs[str(s)]["HRSC_DTM"]
                    if "HRSC_DTM_res" in sounessGLFs[str(s)]:
                        tileres = sounessGLFs[str(s)]["HRSC_DTM_res"]
                    else:
                        tileres = "none "
                    print("S{s}: {t}, resolution {r}m.".format(s=s,
                                                               t=tileused,
                                                               r=tileres))
            print("{n}\n".format(n=notfound))

def plotAll(tilenames, polygons, resolutions):
    for tn, p, r in zip(tilenames, polygons, resolutions):
        print("tile: {t} polygon: {pl} resolution: {r}m".format(t=tn, pl=p,r=r))
        x = [i[0]  for i in p]
        y = [i[1]  for i in p]    
        print(x,y)
        plt.plot(x,y, "k-")
        plt.title("{n} HRSC DTM tiles".format(n=len(tilenames)))
        plt.xlim([-180,180])

def getPolygons_Res(HRSC_DA4_GDALdict):
    """ get the coverage polygons and resolutions """
    tilenames = HRSC_DA4_GDALdict.keys()
    HRSCdata = HRSC_DA4_GDALdict.values()
    latlng_coords =  [v['wgs84Extent']['coordinates'][0] for v in HRSCdata]
    upperLefts = [c[0] for c in latlng_coords]
    upperRights = [c[2] for c in latlng_coords]
    lowerLefts = [c[1] for c in latlng_coords]
    lowerRights = [c[3] for c in latlng_coords]
    polygons = zip(upperLefts, upperRights, lowerRights, lowerLefts, upperLefts)

    geotransf = [v['geoTransform'] for v in HRSCdata]
    res = [g[1] for g in geotransf]

    return tilenames, polygons, res

print_tiles_notused(DTMres, HRSC_da4dict, quiet=True)

#tiles, polys, res = getPolygons_Res(HRSC_da4dict)
#plotAll(tiles, polys, res)
#plt.show()

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
