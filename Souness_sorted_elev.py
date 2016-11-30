# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 12:33:45 2016

@author: David Trethewey
"""
import json
import csv
from operator import itemgetter

sounessjson = "souness_glf.json"

with open(sounessjson) as json_file:
    json_data = json.load(json_file)
    GLFs = json_data['Souness'].items()

    catnums = [g[0] for g in GLFs]
    elevs = [int(g[1]['Elevation'][:-1]) for g in GLFs]
    cat_elev_tup = zip(catnums, elevs)
    cat_elev_tup = sorted(cat_elev_tup, key=itemgetter(1))
    
    lowestelev = cat_elev_tup[:30]
    print("Lowest {n} GLFs (buffer mean from Souness catalog):".format(n=len(lowestelev)))
    print(lowestelev)
    highestelev = cat_elev_tup[-30:]
    highestelev.reverse()
    print("Highest {n} GLFs (buffer mean from Souness catalog):".format(n=len(highestelev)))
    print(highestelev)
    #for g in GLFs:
    #    N = g[0]
    #    attrs = g[1]
    #    print(N, attrs['Elevation'], attrs[])

with open("SounessCatalog_Mars2000EqCyl_lat0_40_combinedstats_allLandSerf3.csv") as csvfile:
    
    spamreader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
    cat_elev_tup = []
    for row in spamreader:
        #print(row)
        cat_elev_tup.append((int(row['CatNumber']), float(row['heads_DTM_avg'])))

cat_elev_tup = sorted(cat_elev_tup, key=itemgetter(1))

lowestelev = cat_elev_tup[:30]
print("Lowest {n} GLFs (head):".format(n=len(lowestelev)))
print(lowestelev)
highestelev = cat_elev_tup[-30:]
highestelev.reverse()
print("Highest {n} GLFs (head):".format(n=len(highestelev)))
print(highestelev)

        
