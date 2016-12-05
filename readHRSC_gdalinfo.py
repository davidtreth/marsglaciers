# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 11:52:16 2016

@author: David Trethewey

This program takes information from the 

DA4, ND4 and layerstack gdalinfo

and outputs it to JSON files

"""

import subprocess
import json
import os.path
import glob


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
HRSC_pathroot =  "/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessCatalog3_backup/"
HRSC_da4dict, HRSC_nd4dict, HRSC_Lyr2dict = readfromHRSCfiles(HRSC_pathroot)
os.chdir(currentdir)

HRSC_da4_jsonfile = "HRSC_da4_gdalinfo.json"
HRSC_nd4_jsonfile = "HRSC_nd4_gdalinfo.json"
HRSC_Lyr_jsonfile = "HRSC_Layerstack10band_gdalinfo.json"
print("Writing JSON. DA4 areoid DTM")
with open(HRSC_da4_jsonfile, "w") as jsonf:
    da4json = json.dump(HRSC_da4dict, jsonf)
print("ND4 nadir image")
with open(HRSC_nd4_jsonfile, "w") as jsonf:
    nd4json = json.dump(HRSC_nd4dict, jsonf)
print("10 band layerstack")
with open(HRSC_Lyr_jsonfile, "w") as jsonf:
    lyrjson = json.dump(HRSC_Lyr2dict, jsonf)
print("Done")
