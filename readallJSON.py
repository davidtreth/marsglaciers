# -*- coding: utf-8 -*-
""" this program reads in the various JSON files into dictionaries """
import json

# the DTM resolutions of all of the HRSC DTM tiles
# intersecting the Souness GLF extents
isect_DTMresJSON = "SounessROIs/HRSC_DTMres_index_extent.json"

# a list of intersecting Souness GLFs for each HRSC DTM tile
isect_DTMSounesslistJSON = "SounessROIs/HRSCdtm_tiles_isect_extent_sounessobjs.json"

# a list of intersecting HRSC DTM tiles for each Souness GLF extent
souness_DTMtiles = "SounessROIs/souness_extent_HRSCdtm_tiles.json"

# a file with various information on each Souness GLF
# the HRSC tiles referenced here are the ones used in the dissertation
souness_GLFsJSON = "souness_glf.json"

# the gdalinfo from the 179 tiles used in the dissertation
#
# firstly the areoid DTM
HRSC_da4_jsonfile = "HRSC_da4_gdalinfo.json"

# then the nadir image (original resolution)
HRSC_nd4_jsonfile = "HRSC_nd4_gdalinfo.json"

# and the 10 band layerstack
HRSC_Lyr_jsonfile = "HRSC_Layerstack10band_gdalinfo.json"

with open(isect_DTMresJSON) as jsonf:
    DTMres = json.load(jsonf)
with open(isect_DTMSounesslistJSON) as jsonf:
    HRSC_Souness = json.load(jsonf)
with open(souness_DTMtiles) as jsonf:
    souness_DTMs = json.load(jsonf)
with open(souness_GLFsJSON) as jsonf:
    sounessGLFs = json.load(jsonf)
    sounessGLFs = sounessGLFs["Souness"]

with open(HRSC_da4_jsonfile) as jsonf:
    HRSC_da4dict = json.load(jsonf)
with open(HRSC_da4_jsonfile) as jsonf:
    HRSC_nd4dict = json.load(jsonf)
with open(HRSC_da4_jsonfile) as jsonf:
    HRSC_Lyr2dict = json.load(jsonf)
