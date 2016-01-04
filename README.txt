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
data from the paper with details of HRSC and HiRISE coverage added by hand


mmc1_HRSC+HiRISE_coverage_duplicates_possible_typos.xls
======================================================
A spreadsheet with some updated notes on the data including the
small number of duplicates and apparent errors in the Souness catalogue

SounessCatalog_converttoMarsEqCyl_lat0_40.py
===========================================
A Python script that reprojects the locations of the Souness objects
from lat/long to the 40° equicylindrical system. The above .csv file
is hardcoded as input and the below .csv as output

mmc1_Souness_alldata.csv
========================
The Souness objects with locations in the equicylindrical system

SounessCatalog_ROIs_shp_allMEqCyl_lat0_40.py
============================================
Creates region of interest shapefiles based on the data in
mmc1_Souness_alldata.csv
The head, terminus, left+right channel points and centre have a circle
of radius 100m defined for them, and an 'extent' is defined from these points
assuming constant channel width, and a 'context' and 'context9' defined
by expanding the extent by factors of 3 and 9 about the centre.

