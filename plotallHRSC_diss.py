# -*- coding: utf-8 -*-
""" plots the footprints of the 179 tiles used in dissertation 
by reading the geometry from the gdalinfo in the JSON file for da4"""

from readallJSON import HRSC_da4dict
from matplotlib import pyplot as plt

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

tiles, polys, res = getPolygons_Res(HRSC_da4dict)
plotAll(tiles, polys, res)
plt.show()

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
