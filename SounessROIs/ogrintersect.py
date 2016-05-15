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

driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(sounessCTX9, 0)
layer = dataSource.GetLayer()


for feature in layer:
    sounessobj = "Souness {s}".format(s=feature.GetField("OBJ_ID"))
    sounesstoptrump = "http://taklowkernewek.neocities.org/mars/souness{s:04d}.html".format(s=int(feature.GetField("OBJ_ID")))
    sounessobjHTML = "<h4><a href='{t}'>{s}</a></h4>".format(s=sounessobj, t=sounesstoptrump)
    prodIDs = []
    # raw_input()
    fid_s = feature.GetFID()
    dataSource2 = driver.Open(hirisedtm, 0)
    layer2 = dataSource2.GetLayer()
    for feature2 in layer2:
        fid_h = feature2.GetFID()
        # if fid_h % 10000 == 0:
        #    print fid_h
        if intersectL(layer, layer2, fid_s, fid_h):
            prodID = feature2.GetField("ProductID")
            if prodID[-8:] == "ANAGLYPH":
                extURL = "http://www.uahirise.org/anaglyph/singula.php?ID="+prodID[:15]
            elif prodID[:5] == "DTEEC":
                extURL = feature2.GetField("ExtURL")
                extURL = "http://www.uahirise.org/dtm/dtm.php?ID="+extURL.split("/")[-1]
            else:
                extURL = feature2.GetField("ExtURL")
            
            linkHTML = "<a href='{e}'>{p}</a>".format(e=extURL, p=prodID)
            prodIDs.append(linkHTML)
    if len(prodIDs) > 0:
        #print(sounessobj)
        #print(prodIDs)
        # sounessobjHTML = "<div class='Sbutton'>" + sounessobjHTML + "</div><br>"
        print(sounessobjHTML)
        for a in prodIDs:
            print(a)
