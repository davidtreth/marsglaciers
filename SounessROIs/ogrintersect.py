from osgeo import ogr
import os

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

souness = "SounessROIextents_all_mars2000.shp"
sounessCTX = "SounessROIcontext_all_Mars2000.shp"
sounessCTX9 = "SounessROIcontext9_all_Mars2000.shp"
hirise = "../hirisecoverage/mars_mro_hirise_rdrv11_c0a.shp"
anaglyph = "../hirisecoverage/mars_mro_hirise_anagly_c0a.shp"
hirisedtm = "../hirisecoverage/mars_mro_hirise_dtm_c0a.shp"

HRSCnd3 = "../HRSCimagecoverage/mars_mex_hrsc_refdr_ND3.shp"
HRSCsr3 = "../HRSCimagecoverage/mars_mex_hrsc_refdr_SR3.shp"


driver = ogr.GetDriverByName("ESRI Shapefile")
sounesslayer = ""
while sounesslayer not in ["e", "c", "9"]:
    sounesslayer = raw_input("Choose Mode (intersect with Souness extents, contexts, or context9 shapefiles. e=extents, c=context 9=context9.\n")
    sounesslayer = sounesslayer.lower()

if sounesslayer == "e":
    dataSource = driver.Open(souness, 0)
elif sounesslayer == "c":
    dataSource = driver.Open(sounessCTX, 0)
elif sounesslayer == "9":
    dataSource = driver.Open(sounessCTX9, 0)
layer = dataSource.GetLayer()


isectlayer = ""
while isectlayer not in ["hi", "a", "d", "nd", "sr"]:
    isectlayer = raw_input("Choose Mode (intersect with Hirise image (hi), Hirise anaglyph (a), Hirise DTM (d), HRSC ND3 images (nd), HRSC SR3 images (sr)).\n")
    isectlayer = isectlayer.lower()



if isectlayer == "nd":
    urltype = raw_input("Use Freie Universitat Berlin URL (b) , NASA PDS orbital data explorer (o) or Arizona State University (a)?")
elif isectlayer == "sr":
    urltype = raw_input("Use NASA PDS orbital data explorer (o) or Arizona State University (a)?") 

def makeURL(urltype, extURL, prodID):
    if urltype == "b":
        return "http://hrscview.fu-berlin.de/cgi-bin/ion-p?page=product2.ion&code=&image="+prodID[1:10].lower()
    elif urltype == "a":
        return "http://viewer.mars.asu.edu/planetview/inst/hrsc/"+prodID[:14].upper()
    else:
        return extURL
    
print(len(layer))

csvmode = raw_input("Use csv output mode? (Y, default is HTML)")
if csvmode.lower() == "y":
    csvmode = True
else:
    csvmode = False

if csvmode:
    if isectlayer in ["nd", "sr"]:
        print("CatNum, {p}".format(p="HRSC_img"))
    else:
        print("CatNum, {p}".format(p="HiRISE_img"))
for feature in layer:
    #print(feature.GetField("OBJ_ID"))
    sounessobj = "Souness {s}".format(s=feature.GetField("OBJ_ID"))
    sounesstoptrump = "http://taklowkernewek.neocities.org/mars/souness{s:04d}.html".format(s=int(feature.GetField("OBJ_ID")))
    sounessobjHTML = "<h4><a href='{t}'>{s}</a></h4>".format(s=sounessobj, t=sounesstoptrump)
    prodIDs = []
    # raw_input()
    fid_s = feature.GetFID()
    
    if isectlayer == "hi":
        dataSource2 = driver.Open(hirise, 0)
    elif isectlayer == "a":
        dataSource2 = driver.Open(anaglyph, 0)
    elif isectlayer == "d":
        dataSource2 = driver.Open(hirisedtm, 0)
    elif isectlayer == "nd":
        dataSource2 = driver.Open(HRSCnd3, 0)
    elif isectlayer == "sr":
        dataSource2 = driver.Open(HRSCsr3, 0)
    layer2 = dataSource2.GetLayer()
    
    for feature2 in layer2:        
        fid_h = feature2.GetFID()        
        #print fid_h
        if intersectL(layer, layer2, fid_s, fid_h):
            prodID = feature2.GetField("ProductID")
            if prodID[-8:] == "ANAGLYPH":
                extURL = "http://www.uahirise.org/anaglyph/singula.php?ID="+prodID[:15]
            elif prodID[:5] == "DTEEC":
                extURL = feature2.GetField("ExtURL")
                extURL = "http://www.uahirise.org/dtm/dtm.php?ID="+extURL.split("/")[-1]
            elif (prodID[-7:] == "ND3.IMG")or(prodID[-7:] == "SR3.IMG"):
                extURL = feature2.GetField("ExtURL")
                extURL = makeURL(urltype, extURL, prodID)
            else:
                extURL = feature2.GetField("ExtURL")
            linkHTML = "<a href='{e}'>{p}</a>".format(e=extURL, p=prodID)
            if csvmode:
                prodIDs.append(prodID)
            else:
                prodIDs.append(linkHTML)
    if len(prodIDs) > 0:
        #print(sounessobj)
        #print(prodIDs)
        # sounessobjHTML = "<div class='Sbutton'>" + sounessobjHTML + "</div><br>"
        if csvmode:
            prodIDstring = ','.join(prodIDs)
            prodIDstring = '"'+prodIDstring+'"'
            print("{s},{p}".format(s=feature.GetField("OBJ_ID"), p=prodIDstring))
        else:
            print(sounessobjHTML)
            for a in prodIDs:
                print(a)
