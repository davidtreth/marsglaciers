# this program finds overlap between the Souness object extents
# context or context9s and the HiRISE images, anaglyphs, and DTMs
# and HRSC footprints
from osgeo import ogr
from collections import defaultdict
import os
import json
import csv
import readBerlin
import argparse

### from https://github.com/csterling/Morps/blob/master/morps.py
### This function checks two features in a file to see if they intersect.
### It takes 4 arguments, f1 for the first file, fid1 for the index of the
### first file's feature, f2 for the second file, fid2 for the index of the
### second file's feature. Returns whether the intersection is True or False.
driverList = {"shp":"ESRI Shapefile","json":"GeoJSON","kml":"KML"}

def intersect(f1,f2,fid1=0,fid2=0,fileType="shp"):
    driver = ogr.GetDriverByName(driverList[fileType])
    
    file1 = driver.Open(f1,0)
    layer1 = file1.GetLayer()
    feat1 = layer1.GetFeature(fid1)
    geom1 = feat1.GetGeometryRef()

    file2 = driver.Open(f2,0)
    layer2 = file2.GetLayer()
    feat2 = layer2.GetFeature(fid2)
    geom2 = feat2.GetGeometryRef()

    if geom1.Intersect(geom2) == 1:
        return True
    else:
        return False
    
### version of the function that takes data layers rather than file names
def intersectL(d1,d2,fid1=0,fid2=0,fileType="shp"):
    feat1 = d1.GetFeature(fid1)
    geom1 = feat1.GetGeometryRef()

    feat2 = d2.GetFeature(fid2)
    geom2 = feat2.GetGeometryRef()

    if geom1.Intersect(geom2) == 1:
        return True
    else:
        return False

def partialL(d1,d2,fid1=0,fid2=0,fileType="shp"):
    """ check for partial coverage """
    feat1 = d1.GetFeature(fid1)
    geom1 = feat1.GetGeometryRef()

    feat2 = d2.GetFeature(fid2)
    geom2 = feat2.GetGeometryRef()

    if geom1.Intersect(geom2) == 1 and geom2.Contains(geom1) == 0:
        return True
    else:
        return False    
def containsL(d1,d2,fid1=0,fid2=0,fileType="shp"):
    """ check if geom2 contains geom1 """
    feat1 = d1.GetFeature(fid1)
    geom1 = feat1.GetGeometryRef()

    feat2 = d2.GetFeature(fid2)
    geom2 = feat2.GetGeometryRef()

    if geom2.Contains(geom1) == 1:
        return True
    else:
        return False    

def makeURL(urltype, extURL, prodID):
    if urltype == "b":
        return "http://hrscview.fu-berlin.de/cgi-bin/ion-p?page=product2.ion&code=&image="+prodID[1:10].lower()
    elif urltype == "a":
        return "http://viewer.mars.asu.edu/planetview/inst/hrsc/"+prodID[:14].upper()
    else:
        return extURL
    
souness = "SounessROIextents_all_mars2000.shp"
sounessCTX = "SounessROIcontext_all_Mars2000.shp"
sounessCTX9 = "SounessROIcontext9_all_Mars2000.shp"
hirise = "../hirisecoverage/mars_mro_hirise_rdrv11_c0a.shp"
anaglyph = "../hirisecoverage/mars_mro_hirise_anagly_c0a.shp"
hirisedtm = "../hirisecoverage/mars_mro_hirise_dtm_c0a.shp"

hirisekw = "../hirisecoverage/mars_mro_hirise_rdrv11_redonly_kernewek_c0a.shp"

HRSCnd3 = "../HRSCimagecoverage/mars_mex_hrsc_refdr_ND3.shp"
HRSCsr3 = "../HRSCimagecoverage/mars_mex_hrsc_refdr_SR3.shp"
HRSCdtm = "../HRSCimagecoverage/mars_mex_hrsc_dtmrdr_c0a.shp"


driver = ogr.GetDriverByName("ESRI Shapefile")

SounessDict = defaultdict(dict)
isectLayerDict = defaultdict(list)
containsLayerDict = defaultdict(list)

sounesslayer = ""
isectlayer = ""
urltype = ""
outputmode = ""

# Create the command line options parser.
parser = argparse.ArgumentParser()
# take the input from a file specified
# by a command line argument
parser.add_argument("-s", type=str,
                    help="Specify the Souness object extent (e), context (c), context9 (9).")
parser.add_argument("-c", type=str,
                    help="Specify the type of coverage layer (HiRise image (hi), Anaglyph (a), HiRISE DTM (d), HiRISE kernewek image (hikw), HRSCND3 images (nd), HRSC SR3 images (sr), HRSC DTMs (dtm)).")
parser.add_argument("-url", type=str,
                    help="Specify URL link to use (for HRSC ND, DTM or SR) b=Berlin, o = NASA PDS orbital data explorer, a=Arizona State University")
parser.add_argument("-out", type=str,
                    help="Specify output mode (c=csv, j=JSON)")
args = parser.parse_args()

if args.s:
	sounesslayer = args.s.lower()
if args.c:
	isectlayer = args.c.lower()
if args.url:
	urltype = args.url.lower()
if args.out:
	outputmode = args.out.lower()

while sounesslayer not in ["e", "c", "9"]:
    sounesslayer = raw_input("Choose Mode (intersect with Souness extents, contexts, or context9 shapefiles. e=extents, c=context 9=context9.\n")
    sounesslayer = sounesslayer.lower()

if sounesslayer == "e":
    dataSource = driver.Open(souness, 0)
    sounesslayer = "extent"
elif sounesslayer == "c":
    dataSource = driver.Open(sounessCTX, 0)
    sounesslayer = "context"
elif sounesslayer == "9":
    dataSource = driver.Open(sounessCTX9, 0)
    sounesslayer = "context9"
layer = dataSource.GetLayer()

#isectmode = ""
#while isectmode not in ["i", "c", "p"]:
#    isectmode = raw_input("Choose intersect mode (i), contains (c), or partial (p) - does the souness object need to be wholly within the coverage geome#try? If 'p' is selected, only partial coverage is returned")
    
    

while isectlayer not in ["hi", "a", "d", "hikw", "nd", "sr", "dtm"]:
    isectlayer = raw_input("Choose Mode (intersect with Hirise image (hi), Hirise anaglyph (a), Hirise DTM (d), HiRISE kernewek image (hikw), HRSCND3 images (nd), HRSC SR3 images (sr), HRSC DTMs (dtm)).\n")
    isectlayer = isectlayer.lower()

if isectlayer in ["nd", "dtm"]:
    while urltype not in ["b", "o", "a"]:
        urltype = raw_input("Use Freie Universitat Berlin URL (b) , NASA PDS orbital data explorer (o) or Arizona State University (a)?")
elif isectlayer == "sr":
    while urltype not in ["o", "a"]:        
        urltype = raw_input("Use NASA PDS orbital data explorer (o) or Arizona State University (a)?") 


    
print(len(layer))

while outputmode.lower() not in ["j", "c"]:#, "h"]:
    outputmode = raw_input("Use csv output mode (c), JSON mode (j)?")#, HTML mode (h)?")

if outputmode == "c":
    if isectlayer in ["nd", "sr"]:
        print("CatNum, {p}".format(p="HRSC_img"))
    elif isectlayer == "dtm":
        print("CatNum, {p}".format(p="HRSC_dtm"))
    else:
        print("CatNum, {p}".format(p="HiRISE_img"))

# put differeny types of footprint into a dictionary to
# save a long if elif ... section
intseclyrDict = {"hi": hirise,
                 "a": anaglyph,
                 "d": hirisedtm,
                 "hikw": hirisekw,
                 "nd": HRSCnd3,
                 "sr": HRSCsr3,
                 "dtm":HRSCdtm}
# for output filename
intsecnameDict = {"hi": "HiRISEimg",
                 "a": "HiRISEana",
                 "d": "HiRISEdtm",
                 "hikw": "HiRISEkw",
                 "nd": "HRSCnd3",
                 "sr": "HRSCsr3",
                 "dtm": "HRSCdtm"}

# to store the resolutions indexed by 1st 5 chars of DTM tile id
DTMresDict = {}
# read from a file if we can
HRSCDTMres_fn = "HRSC_DTMres_index_{e}.json".format(e=sounesslayer)
try:
    with open(HRSCDTMres_fn) as json_file:
        DTMresDict = json.load(json_file)
except IOError:
    print("cannot file file {f}, starting with empty DTMresDict".format(f=HRSCDTMres_fn))

# for debugging
verbose = True

for feature in layer:

    sounessobjID = feature.GetField("OBJ_ID")
    sounessobj = "Souness {s}".format(s=sounessobjID)
    if verbose:
        print(sounessobj)
    sounesstoptrump = "http://taklowkernewek.neocities.org/mars/sounesstoptrumps_js.html?S{s:04d}".format(s=int(sounessobjID))
    sounessobjHTML = "<div><a href='{t}'>{s}</a></div>".format(s=sounessobj, t=sounesstoptrump)
    prodIDs = []
    prodIDs_partial = []
    # store 1 for contains, 0 for partial
    contains = []
    linkHTMLs = []

    fid_s = feature.GetFID()
    dataSource2 = driver.Open(intseclyrDict[isectlayer], 0)

    layer2 = dataSource2.GetLayer()
    
    for feature2 in layer2:        
        fid_h = feature2.GetFID()        
        #print fid_h

        fpContainsS = containsL(layer, layer2, fid_s, fid_h)

        fpIntersS = intersectL(layer, layer2, fid_s, fid_h)

        fpPartialS  = partialL(layer, layer2, fid_s, fid_h)
        if fpIntersS:
            prodID = feature2.GetField("ProductID")
            # use only DA4 from HRSC DTM coverage shapefile
            if prodID[-7:-4] in ["DT4", "GR4", "IR4", "ND4", "RE4", "BL4"]:
                continue
            if prodID[-8:] == "ANAGLYPH":
                extURL = "http://www.uahirise.org/anaglyph/singula.php?ID="+prodID[:15]
            elif prodID[:5] == "DTEEC":
                extURL = feature2.GetField("ExtURL")
                extURL = "http://www.uahirise.org/dtm/dtm.php?ID="+extURL.split("/")[-1]
            elif (prodID[-7:] == "ND3.IMG")or(prodID[-7:] == "SR3.IMG")or(prodID[-7:] == "DA4.IMG"):
                extURL = feature2.GetField("ExtURL")
                extURL = makeURL(urltype, extURL, prodID)

                    
            else:
                extURL = feature2.GetField("ExtURL")
            

            #if outputmode in ["c", "j"]:
            
            prodIDs.append(prodID)
            linkHTMLs.append(extURL)
            if not(containsL(layer, layer2, fid_s, fid_h)):
                prodIDs_partial.append(prodID)
                contains.append(0)
            else:
                contains.append(1)
            

            """
            else:
                linkHTML = "<a href='{e}'>{p}</a>".format(e=extURL, p=prodID)
                linkHTMLs.append(linkHTML)
            """
    if verbose:
        print(zip(prodIDs, contains))
        print(prodIDs_partial)

    if len(prodIDs) > 0:
        if outputmode in ["j", "c"]:
            SounessDict[sounessobjID]['prodIDs'] = prodIDs
            SounessDict[sounessobjID]['containsArr'] = contains
            SounessDict[sounessobjID]['extURLs'] = linkHTMLs
            #if len(prodIDs_partial)>0:
            #    SounessDict[sounessobjID]['prodIDs_partial'] = prodIDs_partial
            for a, c, extURL in zip(prodIDs, contains, linkHTMLs):
                a5 = a[:5]
                if isectlayer == "dtm":
                    if urltype == "b" and a5 not in DTMresDict:
                        DTMres = readBerlin.getAreoidDTMres(extURL)
                    elif isinstance(DTMresDict[a5], float):
                        DTMres = DTMresDict.pop(a5)
                    elif isinstance(DTMresDict[a5]['resolution'], float):
                        DTMres = DTMresDict[a5]['resolution']
                    DTMresDict[a5] = {}
                    DTMresDict[a5]['resolution'] = DTMres
                    DTMresDict[a5]['prodID'] = a
                    DTMresDict[a5]['url'] = extURL                    
                    if sounessobjID not in isectLayerDict[a5]:
                        isectLayerDict[a5].append(sounessobjID)
                    if c and (sounessobjID not in containsLayerDict[a5]):
                        containsLayerDict[a5].append(sounessobjID)
                else:
                    if sounessobjID not in isectLayerDict[a]:
                        isectLayerDict[a].append(sounessobjID)
                    if c and (sounessobjID not in containsLayerDict[a]):
                        containsLayerDict[a].append(sounessobjID)
                    
                    
    """
    elif outputmode == "h":
            print(sounessobjHTML)
            for a in prodIDs:
                print(a)
    """

souness_outfn = "souness_{e}_{fp}_tiles".format(e=sounesslayer, fp=intsecnameDict[isectlayer])                
isectLayer_outfn = "{fp}_tiles_isect_{e}_sounessobjs".format(e=sounesslayer, fp=intsecnameDict[isectlayer])
containsLayer_outfn = "{fp}_tiles_contains_{e}_sounessobjs".format(e=sounesslayer, fp=intsecnameDict[isectlayer])

    
if outputmode == "j":
    souness_outfn += ".json"
    isectLayer_outfn += ".json"
    containsLayer_outfn += ".json"
    print(SounessDict)
    with open(souness_outfn, "w") as outFile:
        SounessJSON = json.dump(SounessDict, outFile)

    print(isectLayerDict)
    with open(isectLayer_outfn, "w") as outFile:
        isectJSON = json.dump(isectLayerDict, outFile)
    print(containsLayerDict)
    with open(containsLayer_outfn, "w") as outFile:
        containsJSON = json.dump(containsLayerDict, outFile)
        
    print(DTMresDict)
    with open(HRSCDTMres_fn, "w") as outFile:
        HRSCDTMRES = json.dump(DTMresDict, outFile)
if outputmode == "c":
    souness_outfn += ".csv"
    isectLayer_outfn += ".csv"
    with open(souness_outfn, "w") as outFile:
        spamwriter = csv.writer(outFile, delimiter=",")
        outRow1 = ['CatNum', 'HiRISE_img', 'ContainsArr']
        spamwriter.writerow(outRow1)
        for s in SounessDict:
            outRow =[s, ",".join(SounessDict[s]['prodIDs']), ",".join([str(c) for c in SounessDict[s]['containsArr']])]
            spamwriter.writerow(outRow)
    with open(isectLayer_outfn, "w") as outFile:
        spamwriter = csv.writer(outFile, delimiter=",")
        for i in isectLayerDict:            
            outRow =[i, ",".join(isectLayerDict[i])]
            spamwriter.writerow(outRow)
        
    
    if verbose:
        prodIDs_all = []
        for s in SounessDict:
            prodIDs_all.extend(SounessDict[s]['prodIDs'])
        prodIDs_all = list(set(prodIDs_all))
        print(prodIDs_all)
        print("number of intersected tile footprints = {n}".format(n=len(prodIDs_all)))
        print("taking first 5 chars")
        prdIDs = [i[:5] for i in prodIDs_all]
        prdIDs = list(set(prdIDs))
        print("number of distinct [:5] tileIDs = {n}".format(n=len(prdIDs)))
