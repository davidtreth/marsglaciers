# David Trethewey 30-08-2014

# assume we are running from */remotesensing_dissertation directory

import os.path
import sys
#import time

#pathtoMOLA = "mola128_88Nto88S_Simp_clon0/mola128_88Nto88S_Simp_clon0/mola128_oc0/w001001.adf"
pathtoMOLA_N = "MOLA_128/MOLA_128_Nmidlat_layerstack.kea"
pathtoMOLA_S = "MOLA_128/MOLA_128_Smidlat_layerstack.kea"

def calcAllStats(heads, centres, termini, heads5km, extents, CTX, CTX9):
	outfileheads_N = heads.split("/")[-1][:-4]+'_N_stats.csv'
	outfilecentres_N = centres.split("/")[-1][:-4]+'_N_stats.csv'
	outfiletermini_N = termini.split("/")[-1][:-4]+'_N_stats.csv'
	outfileheads5km_N = heads5km.split("/")[-1][:-4]+'_N_stats.csv'
	outfileextents_N = extents.split("/")[-1][:-4]+'_N_stats.csv'
	outfileCTX_N = CTX.split("/")[-1][:-4]+'_N_stats.csv'	
	outfileCTX9_N = CTX9.split("/")[-1][:-4]+'_N_stats.csv'
	outfileheads_S = heads.split("/")[-1][:-4]+'_S_stats.csv'
	outfilecentres_S = centres.split("/")[-1][:-4]+'_S_stats.csv'
	outfiletermini_S = termini.split("/")[-1][:-4]+'_S_stats.csv'
	outfileheads5km_S = heads5km.split("/")[-1][:-4]+'_S_stats.csv'
	outfileextents_S = extents.split("/")[-1][:-4]+'_S_stats.csv'
	outfileCTX_S = CTX.split("/")[-1][:-4]+'_S_stats.csv'	
	outfileCTX9_S = CTX9.split("/")[-1][:-4]+'_S_stats.csv'
	zonalstats_cmdlayerstack_heads5km_N = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_N + ' --invector '+heads5km+' --outstats '+ outfileheads5km_N +' --min --max --mean --stddev --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_ext_N = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_N + ' --invector '+extents+' --outstats '+ outfileextents_N +' --min --max --mean --stddev --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_CTX_N = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_N + ' --invector '+CTX+' --outstats '+ outfileCTX_N +' --min --max --mean --stddev --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_CTX9_N = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_N + ' --invector '+CTX9+' --outstats '+ outfileCTX9_N +' --min --max --mean --stddev --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_heads_N = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_N + ' --invector '+heads+' --outstats '+ outfileheads_N +' --mean --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_centres_N = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_N + ' --invector '+centres+' --outstats '+ outfilecentres_N +' --mean --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_termini_N = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_N + ' --invector '+termini+' --outstats '+ outfiletermini_N +' --mean --mode --minThreshold -9998 --force'
	os.system(zonalstats_cmdlayerstack_heads5km_N)	
	os.system(zonalstats_cmdlayerstack_ext_N)	
	os.system(zonalstats_cmdlayerstack_CTX_N)	
	os.system(zonalstats_cmdlayerstack_CTX9_N)	
	os.system(zonalstats_cmdlayerstack_heads_N)
	os.system(zonalstats_cmdlayerstack_centres_N)
	os.system(zonalstats_cmdlayerstack_termini_N)

	zonalstats_cmdlayerstack_heads5km_S = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_S + ' --invector '+heads5km+' --outstats '+ outfileheads5km_S +' --min --max --mean --stddev --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_ext_S = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_S + ' --invector '+extents+' --outstats '+ outfileextents_S +' --min --max --mean --stddev --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_CTX_S = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_S + ' --invector '+CTX+' --outstats '+ outfileCTX_S +' --min --max --mean --stddev --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_CTX9_S = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_S + ' --invector '+CTX9+' --outstats '+ outfileCTX9_S +' --min --max --mean --stddev --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_heads_S = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_S + ' --invector '+heads+' --outstats '+ outfileheads_S +' --mean --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_centres_S = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_S + ' --invector '+centres+' --outstats '+ outfilecentres_S +' --mean --mode --minThreshold -9998 --force'
	zonalstats_cmdlayerstack_termini_S = zonalstats_cmdbase + ' --inimage '+ pathtoMOLA_S + ' --invector '+termini+' --outstats '+ outfiletermini_S +' --mean --mode --minThreshold -9998 --force'
	os.system(zonalstats_cmdlayerstack_heads5km_S)	
	os.system(zonalstats_cmdlayerstack_ext_S)	
	os.system(zonalstats_cmdlayerstack_CTX_S)	
	os.system(zonalstats_cmdlayerstack_CTX9_S)	
	os.system(zonalstats_cmdlayerstack_heads_S)
	os.system(zonalstats_cmdlayerstack_centres_S)
	os.system(zonalstats_cmdlayerstack_termini_S)

zonalstats_cmdbase = 'python PythonScripts/rsgislib_zonalStats_DClewley.py'
heads_GLFs = 'SounessROIs/SounessROIheads_all_Mars2000EqCyl_lat0_40.shp'
centres_GLFs = 'SounessROIs/SounessROIcentres_all_Mars2000EqCyl_lat0_40.shp'
termini_GLFs = 'SounessROIs/SounessROItermini_all_Mars2000EqCyl_lat0_40.shp'
heads5km_GLFs = 'SounessROIs/SounessROIheads5km_all_Mars2000EqCyl_lat0_40.shp'
extents_GLFs = 'SounessROIs/SounessROIextents_all_Mars2000EqCyl_lat0_40.shp'
CTX_GLFs = 'SounessROIs/SounessROIcontext_all_Mars2000EqCyl_lat0_40.shp'
CTX9_GLFs = 'SounessROIs/SounessROIcontext9_all_Mars2000EqCyl_lat0_40.shp'

calcAllStats(heads_GLFs, centres_GLFs, termini_GLFs, heads5km_GLFs, extents_GLFs, CTX_GLFs, CTX9_GLFs)



