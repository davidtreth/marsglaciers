David Trethewey's Martian scripts
=================================

These are primarily based on my 2014 MSc dissertation
on Martian glaciers. Most of these scripts are highly ad-hoc in
nature and this is an attempt to provide a little more regularised
version of these primarily for my own reuse of code towards related
and other projects.

drawCircle.py:
==========
A couple of Python functions that return a list of points
approximating the drawing of a circle with an N sided polygon

mmc1_HRSC+HiRISE_coverage_forsummarystats_cleaned.csv
=====================================================
The data file based on the Souness et al. 2012 table as supplementary
data from the paper with details of HRSC and HiRISE coverage added by hand.
This has a small number of changes made in Sept 2016 after I discovered
I had incorrectly assigned a few HRSC tiles


mmc1_HRSC+HiRISE_coverage_duplicates_possible_typos.xls
======================================================
A spreadsheet with some updated notes on the data including the
small number of duplicates and apparent errors in the Souness catalogue.
This has a small number of changes made in Sept 2016 after I discovered
I had incorrectly assigned a few HRSC tiles

SounessCatalog_converttoMarsEqCyl_lat0_40.py
===========================================
A Python script that reprojects the locations of the Souness objects
from lat/long to the 40° equicylindrical system. The above .csv file
is hardcoded as input and the below .csv as output

mmc1_Souness_alldata.csv
========================
The Souness objects with locations in the equicylindrical system.
This has a small number of changes made in Sept 2016 after I discovered
I had incorrectly assigned a few HRSC tiles.

SounessCatalog_ROIs_shp_allMEqCyl_lat0_40.py
============================================
Creates region of interest shapefiles based on the data in
mmc1_Souness_alldata.csv
The head, terminus, left+right channel points and centre have a circle
of radius 100m defined for them, and an 'extent' is defined from these points
assuming constant channel width, and a 'context' and 'context9' defined
by expanding the extent by factors of 3 and 9 about the centre.
This also now exports the location of the
mid-line of each GLF to ''SounessGLFprofiles.csv'


NOTE - some of the zonal statistics scripts were lost...

python_zonalstats_SounessROIsMars2000Eqcyl_lat0_40_MOLA_layerstack.py
=====================================================================
Make zonal statistics based on MOLA data for the Souness glacier ROIs

python_zonalstats_RandomDataHRSCDTMtiles_Mars2000Eqcyl_lat0_40.py
=================================================================
zonal statistics based on a set of randomised ROIs - this looks like the
easiest base to rewrite back to the Souness ROIs one

python_zonalstats_MOLA_Mars2000Eqcyl_lat0_40_layerstack_combinefiles.py
=====================================================================
Collate the files together for the above zonal statistics

python_zonalstats_SounessROIsHRSCDTMtiles_Mars2000EqCyl_lat0_40.py
==================================================================
rewritten Souness ROIs zonal statistics - not tested yet!

 python_zonalstats_SounessROIs_midpoints_HRSCDTMtiles_Mars2000EqCyl_lat0_40.py
 =============================================================================
 Souness ROIs for midpoints zonal statistics

python_zonalstats_HRSC_Mars2000Eqcyl_lat0_40_layerstack_combinefiles.py
======================================================================
rewritten file to collate Souness ROIs zonal statistics - not tested yet!

rsgislib_zonalStats_DClewley.py
================================
adapted script of Dan Clewley to do the zonal stats


readGLFprofiles.py
==================
reads in the Souness GLF profiles, get elevations with GDAL
and makes PNG files of their profiles

ProfilePNGs
===========
PNG files of the output profiles

Segmentation
============

segmentation_mars_version008b_allLandSerf.py
============================================
the main one for the dissertation results

segmentation_mars_version010_rawasp_allLandSerf.py
=================================================
a different version which also does an 0.04kmsq size
for DTM resolutions better than 125m. Also uses raw aspect
rather than abs(aspect from north)

PopulateStats_HSRC_Mars2000EqCyl_lat0_40_2e5sqm_only_add9999_allLandSerfLayerstacks.py
================================================================================
Add the statistics (without +9999) to the clumps file from segmentation

PopulateStats_HSRC_Mars2000EqCyl_lat0_40_rawAsp_add9999_2e4+2e5sqm_allLandSerfLayerstacks.py
===============================================================================
same but for segmentation from rawAsp using both 2e5 and 4e4 sizes.

python_gdal_polygonize_Mars2000EqCtl_lat0_40_objectsz_2e5sqm_only_add9999_allLandSerfLayerstacks.py
===========================================================================
run gdal_polygonize for all tiles and export RAT to .csv file

python_gdal_polygonize_Mars2000EqCyl_lat0_40_rawAspectLandSerfLayerstacks_objectsz_2e5+4e4sqm.py
============================================================================
same as above but for the newer raw-aspect based 2e5 and 4e4 sqm. segmentations

subset_nd4_test.py
============================================================================
Subset the HRSC nadir image files to the bounding box of the context of
each Souness GLF. Create rasterized images from context, extent and head
shapefiles.
Now also generates DTM images, and layerstacks of HRSC image/DTM/slope.
These are all locally scaled.

SounessTopTrumps.py
============================================================================
Create the index HTML of buttons for each Souness GLF, and the Top Trumps page
for each Souness GLF.
Now also generates a JSON file used by the Javascript version of the Souness Top trumps pages.

marsmap.css
============================================================================
the CSS style file that goes with the HTML generated by SounessTopTrumps.py

HiRISE_kw.ods
============================================================================
a spreadsheet listing all the HiRISE images with a Cornish language title
with their image ID, URL, anaglyphs (as of 14.05.16), description,
longitude (dorhys) and latitude (dorles)

DTMcmap.py
============
converts a series of greyscale images to pseudocolour.

Used for the output DTM images.

SounessROIs/ogrintersect.py
============
check for intersection between the footprints of the Souness objects,
and the HiRISE and HRSC footprints from https://ode.rsl.wustl.edu/mars/coverage/ODE_Mars_shapefile.html

SounessROIs/readBerlin.py
===========================
reads DTM resolution from Freie Universität Berlin website


Summary of steps involved
=========================
Get latest coverage shapefiles from https://ode.rsl.wustl.edu/mars/coverage/ODE_Mars_shapefile.html

use the c0a files

HiRISE image - 
https://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mro/hirise/rdrv11/

HiRISE anaglyphs -
https://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mro/hirise/anagly/

HiRISE DTMs-
https://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mro/hirise/dtm/

HRSC images -
https://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mex/hrsc/refdr3/

select out the nadir image and the "super-resolution" ones by viewing the attribute table in QGIS

Make sure copies of the files are in the hirisecoverage/ and HRSCimagecoverage/ directories

Run the ogrintersect.py file and select options interactively.

For the Top Trumps website, run for each of extents, context, and context9 in csv mode
could automate this...

run the subset_nd4_test.py script to generate the various overlay PNGs

run the SounessTopTrumps.py script to make a new json file
