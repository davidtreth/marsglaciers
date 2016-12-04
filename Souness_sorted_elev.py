# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 12:33:45 2016

@author: David Trethewey
"""
import json
import csv
from operator import itemgetter

sounessjson = "souness_glf.json"

def printTable(tuples):
    """
    expect tuple to be  (CatNum, Elevation, region, regionURL, HRSC_DTM, HRSC_DTM_URL, lat, lng, area, NHiRISE, Nanagl)
    """
    print("<table><tr><th>Catalog number</th><th>Elevation (m)</th><th>Region</th><th>HRSC DTM tile</th><th>Centre Latitude</th><th>Centre Longitude</th><th>Area (sq. km)</th><th>N HiRISE footprints intersecting</th><th>N anaglyphs intersecting</th></tr>")
    
    for s in tuples:
        if s[4] == "none":
            hrsclink = s[4]
        else:
            hrsclink = "<a href='{DTMurl}' target='_blank'>{DTM}</a>".format(DTM=s[4], DTMurl=s[5])
        print("<tr><td><a href='http://taklowkernewek.neocities.org/mars/sounesstoptrumps_js.html?S{N}' target='_blank'>{N}</a></td><td>{e}</td><td><a href='{rURL}' target='_blank'>{r}</a></td><td>{dtmlink}</td><td>{lat:.2f}</td><td>{lng:.2f}</td><td>{a}</td><td>{NH}</td><td>{Nang}</td></tr>".format(
            N=s[0], e=s[1], r=s[2], rURL =s[3], dtmlink=hrsclink, lat=s[6], lng=s[7], a=s[8], NH = s[9], Nang=s[10]))
    print("</table>")

def printTableH(tuples):
    """
    expect tuple to be  (CatNum, elevation_head, elevation_terminus, region, regionURL, HRSC_DTM, HRSC_DTM_URL, headlat, headlng, area, NHiRISE)
    """
    print("<table><tr><th>Catalog number</th><th>Head elevation (m)</th><th>Termimus elevation (m)</th><th>Region</th><th>HRSC DTM tile</th><th>Head Latitude</th><th>Head Longitude</th><th>Area (sq. km)</th><th>N HiRISE footprints intersecting</th><th>N anaglyphs intersecting</th></tr>")
    
    for s in tuples:
        if s[5] == "none":
            hrsclink = s[5]
        else:
            hrsclink = "<a href='{DTMurl}' target='_blank'>{DTM}</a>".format(DTM=s[5], DTMurl=s[6])
        print("<tr><td><a href='http://taklowkernewek.neocities.org/mars/sounesstoptrumps_js.html?S{N}' target='_blank'>{N}</a></td><td>{eH}</td><td>{eT}</td><td><a href='{rURL}' target='_blank'>{r}</a></td><td>{dtmlink}</td><td>{lat:.2f}</td><td>{lng:.2f}</td><td>{a}</td><td>{NH}</td><td>{Nang}</td></tr>".format(
            N=s[0], eH=s[1], eT = s[2], r=s[3], rURL =s[4], dtmlink=hrsclink, lat=s[7], lng=s[8], a=s[9], NH=s[10], Nang=s[11]))
    print("</table>")


    
    
with open(sounessjson) as json_file:
    json_data = json.load(json_file)
    GLFs = json_data['Souness'].items()

HRSC_DTMres_json = "SounessROIs/HRSC_DTMres_index_extent.json"
with open(HRSC_DTMres_json) as json_file:
    HRSC_DTMres = json.load(json_file)

GLFdict = {int(k):v for (k,v) in GLFs}

catnums = [g[0] for g in GLFs]
elevs = [int(g[1]['Elevation'][:-1]) for g in GLFs]
#NHiRISE = [len(g[1]['HiRISE_ext']) for g in GLFs]
regions = [g[1]['region'] for g in GLFs]
regionURLs = [g[1]['regionURL'] for g in GLFs]
HRSC_DTMs = [g[1]['HRSC_DTM'][:10] for g in GLFs]
HRSC_DTM_URLs = []

#print(GLFs[:2])
#print(GLFdict[1])
#print(GLFdict[1].keys())

for g in GLFs:
    try:
        HRSC_DTM_URLs.append(g[1]['HRSC_DTM_URL'])
    except KeyError:
        HRSC_DTM_URLs.append('')
lats = [float(g[1]['Centlat']) for g in GLFs]
longs = [float(g[1]['Centlon']) for g in GLFs]
areas = [g[1]['Area'][:-7] for g in GLFs]
NHiRISE = [len(g[1]['HiRISE_ext']) for g in GLFs]
Nanaglyph = [len(g[1]['anaglyph_ext']) for g in GLFs]


    
cat_elev_tup = zip(catnums, elevs, regions, regionURLs, HRSC_DTMs, HRSC_DTM_URLs, lats, longs, areas, NHiRISE, Nanaglyph)
cat_elev_tup = sorted(cat_elev_tup, key=itemgetter(1))

nTab = 30
lowestelev = cat_elev_tup[:nTab]
print("<h1>Lowest and highest {n} Souness glacier-like forms</h1>".format(n=nTab))

print("<h3>Based on mean elevation of 5km circular radius buffer (from <a href='https://scholar.google.co.uk/scholar?cluster=16408386379845458674' target='_blank'>Souness et al. 2012 paper</a>)</h4>")
print("<h4>Lowest elevation {n} GLFs (buffer mean from Souness catalog):</h3>".format(n=len(lowestelev)))
printTable(lowestelev)

highestelev = cat_elev_tup[(-1*nTab):]
highestelev.reverse()
print("<h4>Highest elevation {n} GLFs (buffer mean from Souness catalog):</h4>".format(n=len(highestelev)))
printTable(highestelev)
    #print(highestelev)
    #for g in GLFs:
    #    N = g[0]
    #    attrs = g[1]
    #    print(N, attrs['Elevation'], attrs[])

with open("SounessCatalog_Mars2000EqCyl_lat0_40_combinedstats_allLandSerf3.csv") as csvfile:
    
    spamreader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
    cat_elev_tup = []
    statsfile_dict = {}
    for row in spamreader:
        #print(row)
        cat_elev_tup.append((int(row['CatNumber']), float(row['heads_DTM_avg'])))
        statsfile_dict[int(row['CatNumber'])] = row

        
cat_elev_tup = sorted(cat_elev_tup, key=itemgetter(1))


print("<h3>Based on mean HRSC DTM elevation of immediate head area (100m radius)</h3>")
lowestelev = cat_elev_tup[:nTab]
print("<h4>Lowest elevation {n} GLFs (head):</h4>".format(n=len(lowestelev)))
#print(lowestelev)
lowestcatnums = [t[0] for t in lowestelev]

tabletuples = []
for N in lowestcatnums:
    HRSC_DTM = GLFdict[N]['HRSC_DTM'][:10]
    if HRSC_DTM == "none":
        HRSC_DTM_url = ""
    else:
        HRSC_DTM_url = GLFdict[N]['HRSC_DTM_URL']
    
    tpl = (N, int(float(statsfile_dict[N]['heads_DTM_avg'])), int(float(statsfile_dict[N]['termini_DTM_avg'])),
           GLFdict[N]['region'], GLFdict[N]['regionURL'],
           HRSC_DTM, HRSC_DTM_url, GLFdict[N]['Headlat'], GLFdict[N]['Headlon'], GLFdict[N]['Area'][:-7], len(GLFdict[N]['HiRISE_ext']),
           len(GLFdict[N]['anaglyph_ext']))
    tabletuples.append(tpl)       
    #print(N, cat_elev_dict[N])

printTableH(tabletuples)

highestelev = cat_elev_tup[(-1*nTab):]
highestelev.reverse()
print("<h4>Highest elevation {n} GLFs (head):</h4>".format(n=len(highestelev)))
highestcatnums = [t[0] for t in highestelev]
tabletuples = []
for N in highestcatnums:
    HRSC_DTM = GLFdict[N]['HRSC_DTM'][:10]
    if HRSC_DTM == "none":
        HRSC_DTM_url = ""
    else:
        HRSC_DTM_url = GLFdict[N]['HRSC_DTM_URL']
    
    tpl = (N, int(float(statsfile_dict[N]['heads_DTM_avg'])), int(float(statsfile_dict[N]['termini_DTM_avg'])),
           GLFdict[N]['region'], GLFdict[N]['regionURL'],
           HRSC_DTM, HRSC_DTM_url, GLFdict[N]['Headlat'], GLFdict[N]['Headlon'], GLFdict[N]['Area'][:-7], len(GLFdict[N]['HiRISE_ext']),
           len(GLFdict[N]['anaglyph_ext']))
    tabletuples.append(tpl)       



#print(highestelev)
printTableH(tabletuples)

        
