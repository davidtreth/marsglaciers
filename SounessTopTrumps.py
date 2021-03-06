# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 12:18:54 2016

@author: David Trethewey
"""
import csv
import glob
import os.path
import sys
import subprocess
import json

# source files hard-coded
#sounessGLFFilePath = "/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/RemoteSensing_fromDropbox/RemoteSensing_fromDropbox_backup/"
sounessGLFFile="mmc1_HRSC+HiRISE_coverage_duplicates_possible_typos.csv"
#sounessGLFFile="mmc1_HRSC+HiRISE_coverage_forsummarystats_cleaned.csv"

ExtSHPsPath = "SounessROIs_individual/Individual/Extent/"
CtxSHPsPath = "SounessROIs_individual/Individual/Context/"
# path to root of HRSC images
HRSCPath = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessCatalog3_backup/'

#Gfilein = sounessGLFFilePath+sounessGLFFile
Gfilein = sounessGLFFile
print(Gfilein)
HiRISE_kw = 'HiRISE_kw.csv'
#HiRISE_CTX9 = 'SounessROIs/hirise_ctx9.csv'
#HiRISE_anaglyph_CTX9 = 'SounessROIs/hirise_anaglyph_ctx9.csv'
#HiRISE_DTM_CTX9 = 'SounessROIs/hiriseDTMs_ctx9.csv'
#HiRISE_EXT = 'SounessROIs/hirise_ext.csv'
#HiRISE_anaglyph_EXT = 'SounessROIs/hirise_anaglyph_ext.csv'

#HRSC_ND3 = 'SounessROIs/HRSC_ND3_ext.csv'
#HRSC_SR3 = 'SounessROIs/HRSC_SR3_ext.csv'

HiRISE_CTX9 = 'SounessROIs/souness_context9_HiRISEimg_tiles.csv'
HiRISE_anaglyph_CTX9 = 'SounessROIs/souness_context9_HiRISEana_tiles.csv'
HiRISE_DTM_CTX9 = 'SounessROIs/souness_context9_HiRISEdtm_tiles.csv'
HiRISE_DTM_EXT = 'SounessROIs/souness_extent_HiRISEdtm_tiles.csv'
HiRISE_EXT = 'SounessROIs/souness_extent_HiRISEimg_tiles.csv'
HiRISE_anaglyph_EXT = 'SounessROIs/souness_extent_HiRISEana_tiles.csv'

HRSC_ND3 = 'SounessROIs/souness_extent_HRSCnd3_tiles.csv'
HRSC_SR3 = 'SounessROIs/souness_extent_HRSCsr3_tiles.csv'

# the headers in sounessGLFFile
fieldnames=['CatNum','CTXimg','Typo','offcent','Duplicate','HRSC_DTM','DTMres','HiRISE',
            'HiRISE_img','HiRISE_anaglyph','HiRISE_DTM','Hemisph','Headlon','Region','Region2',
            'Headlon180','Headlat','Termlon','Termlon180','Termlat','MidchRlon',
            'MidchRlon180','MidchRlat','MidchLlon','MidchLlon180','MidchLlat',
            'Centlon','Centlon180','Centlat','Length','Width','Area','Orientation',
            'MinElev','MaxElev','MeanElev','StdElev','Elongation','Midchlon',
            'Midchlat','distMidCCent','chanwidth','ratiooffset']
# headers in HiRISE_kw.csv
HiRISEkw_headers = ['N', 'imageID', 'URL', 'anaglyphURL', 'Deskrifans', 'Dorhys', 'Dorhys180', 'Dorles']

HiRISE_CTX9_headers = ['CatNum', 'HiRISE_img', 'ContainsArr']
HRSC_ND3_EXT_headers = ['CatNum', 'HRSC_img']

Sindex = {}

# a few functions for making an HTML colour from a lat, long
# -90 = 0, +90 = 255
def lat_to_blue(lat):
    return int(255 * (lat+90.0)/180.0) 

# -180 = 0, +180 = 255
def long_to_green(lng):    
    return int(255 * (lng+180)/360.0)

def html_colour(lat,lng):
    blue = hex(lat_to_blue(lat))[2:]
    green = hex(long_to_green(lng))[2:]
    red = "ff"
    htmlcolour = "#" + str(red).zfill(2) + str(green).zfill(2) + str(blue).zfill(2)
    return htmlcolour


# find what to set the top and left CSS parameters for
# the div that sets the marker position placing the GLF on the background map
# set to a 800x400px map by default
# that goes up to 70° latitude
def lat_to_top(lat, height=400,zerop=16):
    return ((70. - lat)/140.)*height - zerop

def lng_to_left(lng, width=800,zerop=10):
    return ((180. + lng)/360.)*width - zerop


""" def makeImageFileCrop(n, cropshp):
    # crop an image to context shapefile cutline 
    # nadir image file n
    outfile = 'Souness_'+str(indshp+1)+'_CTX_nd4.kea'
    outfile = sounessGLFFilePath + outfile
    IMGFile = HRSCPath + HRSC + '/' + n
    print("shapefile: {s}, image: {n}, outfile: {o}".format(s=cropshp, n=n, o=outfile))
    cmd_subset = "gdalwarp -of KEA -cutline " + shapefile+ " -crop_to_cutline " + n + " " + outfile
    print(cmd_subset)                    
    os.chdir("LandSerf")
    sixbandfile = glob.glob('h'+HRSC+"*rawAsp.kea")
    for sf in sixbandfile:
        outfile2 = 'Souness_'+str(indshp+1)+'_CTX_6band.kea'
        outfile2 = sounessGLFFilePath + outfile2
        print("shapefile: {s}, image: {n}, outfile: {o}".format(s=cropshp, n=sf, o=outfile2))
        cmd_subset = "gdalwarp -of KEA -cutline " + shapefile+ " -crop_to_cutline " + s + " " + outfile2
        subprocess.call(cmd_subset,shell=True)
        os.chdir("..")
        pngout = outfile[:-4]+".png"
        convPNG = "gdal_translate -of PNG "+outfile+ " "+pngout
        subprocess.call(convPNG,shell=True)"""
        

def printButton(GLF,cl="Sbutton"):
    """ GLF is a dictionary, based on a row of the input file. calls html_colour() to decide background
    colour of button """
    lat = float(GLF['Centlat'])
    lng = float(GLF['Centlon180'])

    #buttonHTML = "<div class=\'{cl}\' style=\'background-color:{bcl};\'><a href=\'souness{n:04d}.html\'>Souness {n}</a></div>".format(cl=cl,bcl=html_colour(lat,lng),n=int(GLF['CatNum']))
    buttonHTML = "<div class=\'{cl}\' style=\'background-color:{bcl};\'><a href=\'sounesstoptrumps_js.html?S{n:04d}\'>Souness {n}</a></div>".format(cl=cl,bcl=html_colour(lat,lng),n=int(GLF['CatNum']))
    print(buttonHTML)
    return buttonHTML

def printButton2(n,cl="Sbutton"):
    """ a button which hardcodes a colour based on a lat,long of 0,0 """
    buttonHTML = "<div class=\'{cl}\' style=\'background-color:{bcl};\'><a href=\'souness{n:04d}.html\'>Souness {n}</a></div>".format(cl=cl,bcl=html_colour(0,0),n=n)
    return buttonHTML

def printButtonIndex(cl="Sbutton"):
    """" print the button that goes back to the index of Souness top trumps """
    buttonHTML = "<div class=\'{cl}\' style=\'background-color:{bcl};\'><a href=\'sounesstoptrumps.html\'>Back to Index</a></div>".format(cl=cl,bcl=html_colour(0,0))
    return buttonHTML

def printAnaglyphLink(GLF, useCTX9=False):
    linkHTML = "<div class='anaglink'><h4><a href='sounesstoptrumps_js.html?S{catnum:04d}'>Souness {catnum}</a></h4>".format(catnum=int(GLF['CatNum']))
    if useCTX9:
        # the manually specified ones
        anaglyphimgs = GLF['HiRISE_anaglyph'].split(',')
        # automatically CTX9 intersected ones
        aglyphs = HiRISE_anaglyph_index.get(GLF['CatNum'], [])
        for a in anaglyphimgs:
            if a not in aglyphs:
                aglyphs.append(a)
    else:
        # automatically EXT intersected ones
        aglyphs = HiRISE_ext_anaglyph_index.get(GLF['CatNum'], [])
    for a in aglyphs:
        a = a.lstrip()
        link = "<a href='http://www.uahirise.org/anaglyph/singula.php?ID={anagID}'>{anag}</a>".format(anagID=a[:15], anag=a)
        linkHTML += link
    linkHTML += "</div>"
    return linkHTML
    
def printDTMLink(GLF, useCTX9=False):
    linkHTML = "<div class='anaglink'><h4><a href='sounesstoptrumps_js.html?S{catnum:04d}'>Souness {catnum}</a></h4>".format(catnum=int(GLF['CatNum']))
    if useCTX9:
        # the manually specified ones
        dtmimgs = GLF['HiRISE_DTM'].split(',')
        # automatically CTX9 intersected ones
        dtmimgs2 = HiRISE_DTM_index.get(GLF['CatNum'], [])
        for d in dtmimgs:
            if d not in dtmimgs2:
                dtmimgs2.append(d)
    else:
        # automatically EXT intersected ones
        dtmimgs2 = HiRISE_ext_DTM_index.get(GLF['CatNum'], [])
    for d in dtmimgs2:
        d=d.lstrip()
        imgn = d[6:12]
        try:
            if int(imgn) >= 10000:
                dtm = d[:17].replace("DTEEC","ESP").replace("DTEED","ESP")
            else:
                dtm = d[:17].replace("DTEEC","PSP").replace("DTEED","ESP")         
            link = "<a href='http://www.uahirise.org/dtm/dtm.php?ID={dtmID}'>{dtmfull}</a>".format(dtmID=dtm, dtmfull=d)
            linkHTML += link
        except:
            pass
    linkHTML += "</div>"
    return linkHTML
    
        
    

def checkbounds(bounds=None):
    """ check that a lat/long box is valid """
    try:
        assert(len(bounds) == 4)
        longmin, longmax, latmin, latmax = bounds
        assert (longmin >= -180 and longmin < 180)
        assert (longmax >= -180 and longmax <= 180)
        assert (latmin >= -90 and latmin < 90)
        assert (latmax >= -90 and latmax <= 90)
        assert (longmin != longmax)
        assert (latmin != latmax)
        
        if longmin > longmax:
            tmp = longmin
            longmin = longmax
            longmax = tmp
        if latmin > latmax:
            tmp = longmin
            longmin = longmax
            longmax = tmp                                       
    except:
        # if invalid bounds, set to whole planet
        return([-180.0, 180.0, -90.0, 90.0])
    return [longmin, longmax, latmin, latmax]

def checkinbounds(lng, lat, bounds):
    longmin, longmax, latmin, latmax = bounds
    if lng >= longmin and lng <= longmax and lat >= latmin and lat <= latmax:
        return True
    else:
        return False
def findregion(lng, lat):
    for r in regiondict.keys():
        if checkinbounds(lng, lat, regiondict[r]):
            return r
    return ''

def printHiRISE_kw(bounds=None):
    bounds = checkbounds(bounds)
    output = ""
    with open(HiRISE_kw) as csvfile:
        spamreader = csv.DictReader(csvfile, fieldnames=HiRISEkw_headers,delimiter=',',quotechar='"')
        for row in spamreader:
            if row['N'] == 'N':
                pass
            else:
                lng, lat = float(row['Dorhys180']), float(row['Dorles'])
                if checkinbounds(lng, lat, bounds):
                    output += "<div class='HiRISErow'>"
                    print("<div class='HiRISErow'>")
                    print("<div class='HiRISEkw'><a href='{u}' target='_blank'>{d}</a>. <div class='latlong'>Lat: {t}, Long: {n}</div></div>".format(u=row['URL'], d=row['Deskrifans'], t=int(lat), n=int(lng)))
                    output += "<div class='HiRISEkw'><a href='{u}' target='_blank'>{d}</a>. <div class='latlong'>Lat: {t}, Long: {n}</div></div>".format(u=row['URL'], d=row['Deskrifans'], t=int(lat), n=int(lng))
                    if row['anaglyphURL'] != "":
                        print("<div class='HiRISE3D'><a href='{u}' target='_blank'>{an}</a></div>".format(u=row['anaglyphURL'], an="Red/blue 3D anaglyph"))
                        output += "\n<div class='HiRISE3D'><a href='{u}' target='_blank'>{an}</a></div>".format(u=row['anaglyphURL'], an="Red/blue 3D anaglyph")
                    print("</div>")
                    output += "</div>\n"
    return output

def makeURL(urltype, prodID):
    if urltype == "b":
        return "http://hrscview.fu-berlin.de/cgi-bin/ion-p?page=product2.ion&code=&image="+prodID[1:10].lower()
    elif urltype == "a":
        return "http://viewer.mars.asu.edu/planetview/inst/hrsc/"+prodID[:14].upper()
    else:
        return "http://ode.rsl.wustl.edu/mars/indexproductpage.aspx?product_id="+prodID.upper()

def writeHTMLbuttons(bounds=None, outHTML=None, writeonly3D=True, writeonlyDTM = False, allowCTX9=False):
    """ write out the buttons for the Souness Top Trumps index 
    by default written in rows of 10 buttons """    
    print("<div class='GLFrow'>")
    if outHTML:
        outFile = open(outHTML,"w")
        if not(writeonly3D):
            if bounds:
                outFile.write('<h2 id="toptrumps">Links to individual pages on Souness GLFs in this region</h2>')
            outFile.write("<div class='GLFrow'>")
    spamreader = csv.DictReader(csvfile, fieldnames=fieldnames,delimiter=';',quotechar='"')
    Nbuttons_printed = 0
    for row in spamreader:
        # expect bounds to be a 4 element list [longmin, longmax, latmin, latmax]
        # if they aren't valid, checkbounds will set to whole planet
        bounds = checkbounds(bounds)
        #print("Catalogue number {c}".format(c=row['CatNum']))        
        catnum = row['CatNum']
        # the Sindex dictionary of dictionaries will later be used
        Sindex[catnum] = row        
        if catnum == "Catalogue number":
            # ignore the header row
            pass
        else:
            lng, lat = float(row['Centlon180']), float(row['Centlat'])
            if checkinbounds(lng, lat, bounds):
                if writeonlyDTM:
                    b = ''
                    if allowCTX9:
                        if row['HiRISE_DTM'] != '' or catnum in HiRISE_DTM_index:
                            # set a different CSS class for GLFs with DTMs
                            #b = printButton(row,"anaglink")
                            b = printDTMLink(row, True)
                    else:
                        #if HiRISE_ext_anaglyph_index.has_key(catnum):
                        if catnum in HiRISE_ext_DTM_index:
                            #b = printButton(row,"anaglink")
                            b = printDTMLink(row, False)                    
                elif writeonly3D:
                    b = ''
                    if allowCTX9:
                        if row['HiRISE_anaglyph'] != '' or catnum in HiRISE_anaglyph_index:
                            # set a different CSS class for GLFs with anaglyphs
                            #b = printButton(row,"anaglink")
                            b = printAnaglyphLink(row, True)
                    else:
                        #if HiRISE_ext_anaglyph_index.has_key(catnum):
                        if catnum in HiRISE_ext_anaglyph_index:
                            #b = printButton(row,"anaglink")
                            b = printAnaglyphLink(row, False)                    
                else:
                    #if HiRISE_ext_anaglyph_index.has_key(catnum):
                    if catnum in HiRISE_ext_anaglyph_index:
                        c = "Sbutton3D"
                    else:
                        c = "Sbutton"
                    b = printButton(row, c)
                if outHTML:
                    outFile.write(b)
                    if b != '':
                        outFile.write("\n")
                        Nbuttons_printed += 1
                # once every 10, end the row and start another
                if Nbuttons_printed > 0 and (int(Nbuttons_printed) % 10 == 0):
                    Nbuttons_printed = 0
                    if outHTML and not(writeonly3D):
                        outFile.write("</div><div class='GLFrow'>")
                    print("</div><div class='GLFrow'>")
    if outHTML:
        outFile.write("</div>")
    print("</div>")
        
def writeHTML(GLF):
    """ write the HTML for each GLF's page """
    outHTMLFILE = "souness{n:04d}.html".format(n=int(GLF['CatNum']))
    title = "Souness "+GLF['CatNum']
    # previous and next 
    num = int(GLF['CatNum'])
    if num > 1:
        prev = num-1
    else:
        prev = num
    if num < 1309:
        nextn = num+1
    else:
        nextn = num
    if Sindex[str(prev)]['HiRISE_anaglyph'] != '' or str(prev) in HiRISE_anaglyph_index:
        previous = printButton(Sindex[str(prev)],'Sbutton3D')
    else:
        previous = printButton(Sindex[str(prev)])
    if Sindex[str(nextn)]['HiRISE_anaglyph'] != '' or str(nextn) in HiRISE_anaglyph_index:
        nextone = printButton(Sindex[str(nextn)],'Sbutton3D')
    else:        
        nextone = printButton(Sindex[str(nextn)])
    backindex = "<br>"+printButtonIndex()
    # boilerplate HTML
    introHTML="""<!DOCTYPE html>\n<html>\n<head><meta charset="UTF-8"><link href="../style.css" rel="stylesheet" type="text/css" media="all"><link href="marsmap.css" rel="stylesheet" type="text/css" media="all"><title>{t}</title></head>""".format(t=title)
    # menu bar on my neocities website
    introHTML2=""" <body><div id="header"><img class="flagl"  src="./neocities_marsL.png" alt="3 GLFs in Deuteronilus Mensae" /><div id = "pagetitle"><h2>Souness Glacial-like-form Top Trumps</h2><p class="h3trans">Top Trumps Rewlivaow Meurth Souness</p></div><img class="flagr" src="./neocities_marsR.png" alt="Crater in SE Highlands with GLFs" /></div>
    <nav class="horiz">
      <ul>
      <li><a href="../index.html">Home<br><div class="transtext">Tre</div></a></li>
      <li><a href="../NLPkernewek.html">Cornish NLP<br><div class="transtext">NLP Kernewek</div></a></li>
      <li><a href="../yethanwerin.html">Yeth an Werin map<br><div class="transtext">Map Yeth an Werin</div></a></li>
      <li><a href="../minescornwall_test_stjust.html">Mines of Cornwall maps<br><div class="transtext">Mappys Balyow Kernow</div></a></li>
      <li><a href="../KernowQGIS.html">Maps of Cornwall in Cornish<br><div class="transtext">Mappys Kernow Kernewek</div></a></li>
      <li><a href="../othermaps.html">Other Map Projects<br><div class="transtext">Mappys Erell</div></a></li>
      <li><a href="../aboutauthor.html">About me<br><div class="transtext">A-dro dhymm</div></a></li>
      </ul>
    </nav>
        <nav class="horiz horizL2">
      <ul>
    <li ><a href="index.html">Martian Glacier index map<br><div class="transtext">Map Rewivaow Meurth</div></a></li>
    <li><a href="hemispheres.html">Martian Hemispheric zoomable maps<br><div class="transtext">Mappys Zoumadow Hanter-Bys Meurth</div></a></li>
    <li><a href="regions.html">Martian Regional zoomable maps<br><div class="transtext">Mappys Zoumadow Ranndiryel Meurth</div></a></li>
        <li class="activenav"><a href="sounesstoptrumps.html">Souness Catalogue Top Trump index<br><div class=transtext>Menegva Top Trump Souness</div></a></li>
        <!--<li><a href="mappys/osm_names_kw/index.html">Map source data<br><div class="transtext">Fenten data an mappys</div></a></li>-->
      </ul>
    </nav>"""
    # title
    mainheader = "<h1>"+title+"</h1>"
    # a 800x400px map of Mars is shown
    backgroundimg =  "OverviewMap800px.png"
    backgroundHTML = "<div style='background-image: url({bgr}); height: 400px; width: 800px;'><div class='markercont' style='top: {t}px; left: {l}px;'><div id='diamond-narrow'></div></div></div>".format(bgr=backgroundimg,t=int(lat_to_top(float(row['Centlat']))), l=int(lng_to_left(float(row['Centlon180']))))
    # table with the data
    theaders = "<th>Category</th><th>Value</th>"
    longit = "<td>Centre longitude:</td><td>{l:.2f}</td>".format(l=float(row['Centlon180']))
    latit = "<td>Centre latitude:</td><td>{t:.2f}</td>".format(t=float(row['Centlat']))
    htmlcolour = html_colour(float(row['Centlat']), float(row['Centlon180']))
    regionname = findregion(float(row['Centlon180']), float(row['Centlat']))
    region = "<td>Region:</td><td><a href='{rU}'>{r}</a></td>".format(r=regionname, rU = regionURLdict[regionname])
    # HRSC DTM data
    if row['HRSC_DTM'] == 'none':
        hrsc = "<td>Mars Express DTM coverage:</td><td>{h}</td>".format(h=row['HRSC_DTM'])
    else:
        pdsurl = 'http://pds-geosciences.wustl.edu/mex/mex-m-hrsc-5-refdr-dtm-v1/mexhrs_2001/extras/'
        dtmdir = 'h{n}xxx'.format(n=row['HRSC_DTM'][1])
        extrafile = '{n}.png'.format(n=row['HRSC_DTM'][:10].lower())
        linktoextra = pdsurl + dtmdir + '/' + extrafile
        hrsc = "<td>Mars Express DTM coverage:</td><td> <a href='{hr}'>{h}</a>.\nDTM resolution {r}m</td>".format(hr=linktoextra, h=row['HRSC_DTM'],r=row['DTMres'])

    # HiRISE images
    hiriseimgs = GLF['HiRISE_img'].split(',')
    hiriseimg2 = HiRISE_index.get(GLF['CatNum'], [])
    # remove excess whitespace
    hiriseimgs = [h.strip() for h in hiriseimgs]
    hiriseimg2 = [h.strip() for h in hiriseimg2]
    for himg in hiriseimg2:
        # don't duplicate what was already manually specified
        # and don't include the COLOR ones since we take the
        # first 15 characters which are the same
        # the COLOR image will have the same extent or less
        if himg not in hiriseimgs and "COLOR" not in himg:
            hiriseimgs.append(himg)
            
    hirise = "<td>HiRISE coverage:</td><td>"
    for himg in hiriseimgs:
        himg = himg.lstrip()
        hiriseurl = "http://hirise.lpl.arizona.edu/" + himg[:15] 
        hirise += "<a href='{hiURL}'>{hi}</a> ".format(hiURL=hiriseurl, hi=himg[:15])
    hirise += '</td>'
    # HiRISE anaglyphs
    anaglyphimgs = GLF['HiRISE_anaglyph'].split(',')
    hiriseanag2 = HiRISE_anaglyph_index.get(GLF['CatNum'], [])
    # remove excess whitespace
    anaglyphimgs = [h.strip() for h in anaglyphimgs]
    hiriseanag2 = [h.strip() for h in hiriseanag2]
    
    for aimg in hiriseanag2:
        if aimg not in anaglyphimgs:
            anaglyphimgs.append(aimg)
    anaglyph = "<td>HiRISE anaglyph:</td><td>"
    for aimg in anaglyphimgs:
        anaglyphurl = "http://hirise.lpl.arizona.edu/anaglyph/singula.php?ID="
        aimg = aimg.lstrip()
        leftobs = aimg[:15]
        anaglyphurl = anaglyphurl+leftobs
        anaglyph += "<a href='{aURL}'>{a}</a> ".format(aURL=anaglyphurl, a=aimg)
    anaglyph += '</td>'
    # HiRISE DTMs
    hiriseDTMs = GLF['HiRISE_DTM'].split(',')
    hiriseDTM2 = HiRISE_DTM_index.get(GLF['CatNum'], [])
    
    hiriseDTMs = [h.strip() for h in hiriseDTMs]
    hiriseDTM2 = [h.strip() for h in hiriseDTM2]
    for dimg in hiriseDTM2:
        if dimg not in hiriseDTMs:
            hiriseDTMs.append(dimg)
    hiriseDTM = "<td>HiRISE DTM:</td><td>"
    #if GLF['HiRISE_DTM'] != '':
    # print(hiriseDTMs)
    if hiriseDTMs == ['']:
        hiriseDTMs = []
    for dimg in hiriseDTMs:
        #print(dimg)
        DTMurl = "http://www.uahirise.org/dtm/dtm.php?ID="
        # find the link to the HiRISE website
        dimg=dimg.lstrip()
        imgn = dimg[6:12]
        #print(imgn)
        #raw_input()
        try:
            # if there is no DTM, skip over this code
            if int(imgn) >= 10000:
                dtm = dimg[:17].replace("DTEEC","ESP").replace("DTEED","ESP")
            else:
                dtm = dimg[:17].replace("DTEEC","PSP").replace("DTEED","ESP")
            DTMurl = DTMurl + dtm
            hiriseDTM += "<a href='{dURL}'>{dimg}</a> ".format(dURL=DTMurl, dimg=dimg)
        except:
            pass
    hiriseDTM += "</td>"

    # parameters from the Souness et al. paper
    length = "<td>Length:</td><td>{l:.2f} km</td>".format(l=float(GLF['Length']))
    width = "<td>Width:</td><td>{w:.2f} km</td>".format(w=float(GLF['Width']))
    area = "<td>Area:</td><td>{A:.2f} km sq.</td>".format(A=float(GLF['Area']))
    meanelev = "<td>Elevation (mean of buffer from Souness et al. 2012):</td><td>{e:.0f}m</td>".format(e=float(GLF['MeanElev']))
    orientation = "<td>Orientation:</td><td>{r:.2f} degrees.</td>".format(r=float(GLF['Orientation']))

    # make the table rows
    listitems = [theaders,longit,latit, region, hrsc,hirise,anaglyph,hiriseDTM, length,width,area,meanelev,orientation]
    listitemsHTML = ["<tr>"+i+"</tr>\n" for i in listitems]
    listHTML = "<table class='toptrumptb'>" +"".join(listitemsHTML) +"</table>"
    
    # the subsetted images and rasterized shapefiles
    imagefile = "context_subsets/Souness{i:04d}_context2.png".format(i=int(GLF['CatNum']))
    ctxshapefile = "context_subsets/Souness{i:04d}_contextSHP2.png".format(i=int(GLF['CatNum']))
    extshapefile = "context_subsets/Souness{i:04d}_extentSHP2.png".format(i=int(GLF['CatNum']))
    headshapefile = "context_subsets/Souness{i:04d}_headSHP2.png".format(i=int(GLF['CatNum']))
    imageHTML = "<figure class='hrscnd' style='background-image: url({nd4}); background-repeat: no-repeat;'><img class=\'CTXshp\' src=\'{s}\'></img><img class=\'Headshp\' src=\'{h}\'></img><figcaption>Part of the High Resolution Stereo Camera nadir image. The image is clipped to the bounding box of the \'context\' shapefile, which is 3 times that of the extent of the GLF in each dimension but centred at the same point. The extent itself is overplotted with partial transparency, with the head marked with a white circle.</figcaption></figure>".format(nd4=imagefile, s=extshapefile,h=headshapefile)

    # DTM stats
    DTMstatsfile = "context_subsets/Souness{i:04d}DTM_context.txt".format(i=int(GLF['CatNum']))
    # nadir image dimensions
    NadirDims = "context_subsets/Souness{i:04d}_context.txt".format(i=int(GLF['CatNum']))
    # LnKHead stats file
    LnKHeadstatsfile = "context_subsets/Souness{i:04d}LnKhead.txt".format(i=int(GLF['CatNum']))
    
    # elevation and slope profiles
    profiles = glob.glob("ProfilePNGs/*Cat{i:04d}*.png".format(i=int(GLF['CatNum'])))
    profilesHTML = ["<img class =\'profImage\' src=\'{s}\'></img>\n".format(s=p) for p in profiles]
    profilesHTML.sort()
    profHTML = "".join(profilesHTML)
    
    tagline = "<p>Mars Express <a href=\'http://hrscview.fu-berlin.de/cgi-bin/ion-p?page=entry2.ion'>High Resolution Stereo Camera (link to HRSCView at Freie Universität Berlin)</a> data courtesy of the European Space Agency.</p>"

    # write the HTML to the output file
    with open(outHTMLFILE,"w") as outFile:
        outFile.write(introHTML)
        outFile.write(introHTML2)
        outFile.write(mainheader)
        outFile.write(previous)
        outFile.write(nextone)
        outFile.write(backindex)        
        outFile.write(backgroundHTML)
        outFile.write(listHTML)
        if row['HRSC_DTM'] != 'none':
            outFile.write(imageHTML)
            outFile.write(profHTML)
            outFile.write(tagline)
        outFile.close()
    #print(mainheader)
    #print(listHTML)
    #print(profHTML)


def readDTMStats(statsFileName):
    fieldnames = ['Min', 'Max', 'Mean', 'StdDev', 'Sum']
    with open(statsFileName, "r") as statsFile:
        spamreader = csv.DictReader(statsFile, fieldnames=fieldnames)
        for s in spamreader:
            if s['Min'] == 'Min':
                pass
            else:
                minDTM = float(s['Min']) - 9999.0
                maxDTM = float(s['Max']) - 9999.0
                meanDTM = float(s['Mean']) - 9999.0
                stdDTM =  float(s['StdDev'])
    minDTM = "{m:.0f}".format(m=minDTM)
    maxDTM = "{m:.0f}".format(m=maxDTM)
    meanDTM = "{m:.01f}".format(m=meanDTM)
    stdDTM = "{m:.01f}".format(m=stdDTM)
    stats = {'Min':minDTM, 'Max':maxDTM, 'meanDTM':meanDTM, 'stdDTM':stdDTM}
    print(stats)
    return stats

def readNadirDims(NDFileName):
    fieldnames = ['Width', 'Height', 'PixelScale']
    with open(NDFileName, "r") as NDFile:
        spamreader = csv.DictReader(NDFile, fieldnames=fieldnames)
        for s in spamreader:
            if s['Width'] == 'Width':
                pass
            else:
                width = s['Width']
                height = s['Height']
                psize = round(float(s['PixelScale']),2)
    stats = {'Width': width, 'Height': height, 'PixelScale':psize}
    return stats

def readLnKStats(statsFileName):
    fieldnames = ['Min', 'Max', 'Mean', 'StdDev', 'Sum']
    with open(statsFileName, "r") as statsFile:
        spamreader = csv.DictReader(statsFile, fieldnames=fieldnames)
        for s in spamreader:
            if s['Min'] == 'Min':
                pass
            else:
                minDTM = float(s['Min']) + 12
                maxDTM = float(s['Max']) + 12 
                meanDTM = float(s['Mean']) + 12
                stdDTM =  float(s['StdDev'])
    minDTM = "{m:.03f}".format(m=minDTM)
    maxDTM = "{m:.03f}".format(m=maxDTM)
    meanDTM = "{m:.03f}".format(m=meanDTM)
    stdDTM = "{m:.03f}".format(m=stdDTM)
    stats = {'Min':minDTM, 'Max':maxDTM, 'Mean':meanDTM, 'StdDev':stdDTM}
    print(stats)
    return stats

    
    
def createJSONObj(GLF):
    """ create a JSON object for a GLF """
    glfJSON = {}
    # previous and next 
    num = int(GLF['CatNum'])
    if num > 1:
        prev = num-1
    else:
        prev = num
    if num < 1309:
        nextn = num+1
    else:
        nextn = num
    glfJSON['CatNum'] = num
    glfJSON['CTXimgID'] = GLF['CTXimg']
    glfJSON['previous'] = prev
    glfJSON['next'] = nextn
    glfJSON['Centlon'] = round(float(GLF['Centlon180']),3)
    glfJSON['Centlat'] = round(float(GLF['Centlat']),3)
    glfJSON['Headlat'] = round(float(GLF['Headlat']),3)
    glfJSON['Headlon'] = round(float(GLF['Headlon180']),3)
    glfJSON['htmlcolour'] = html_colour(float(row['Centlat']), float(row['Centlon180']))
    glfJSON['region'] = findregion(float(row['Centlon180']), float(row['Centlat']))
    glfJSON['regionURL'] = regionURLdict[glfJSON['region']]
    # Mars Express DTM
    if GLF['HRSC_DTM'] == 'none':
        glfJSON['HRSC_DTM'] = 'none'
        glfJSON['HRSC_DTM_URL'] = ''
    else:
        #pdsurl = 'http://pds-geosciences.wustl.edu/mex/mex-m-hrsc-5-refdr-dtm-v1/mexhrs_2001/extras/'
        imageexurlbase = 'http://viewer.mars.asu.edu/viewer/hrsc/'
        #dtmdir = 'h{n}xxx'.format(n=GLF['HRSC_DTM'][1])
        #extrafile = '{n}.png'.format(n=GLF['HRSC_DTM'][:10].lower())
        #linktoextra = pdsurl + dtmdir + '/' + extrafile
        imageexurl = imageexurlbase + GLF['HRSC_DTM'][:14]
        glfJSON['HRSC_DTM'] = GLF['HRSC_DTM']
        #glfJSON['HSRC_DTM_URL'] = linktoextra
        glfJSON['HRSC_DTM_URL'] = imageexurl
        glfJSON['HRSC_DTM_res'] = GLF['DTMres']
        
    # HRSC ND3 images
    HRSC_ND3imgs = HRSC_ND3_index.get(GLF['CatNum'], [])
    HRSC_ND3_URLs_ODE = []
    HRSC_ND3_URLs_ASU = []
    HRSC_ND3_URLs_BER = []
    for himg in HRSC_ND3imgs:
        HRSC_URL_o = makeURL("o", himg)
        HRSC_URL_a = makeURL("a", himg)
        HRSC_URL_b = makeURL("b", himg)
        HRSC_ND3_URLs_ODE.append(HRSC_URL_o)
        HRSC_ND3_URLs_ASU.append(HRSC_URL_a)
        HRSC_ND3_URLs_BER.append(HRSC_URL_b)
    HRSC_tuples = list(zip(HRSC_ND3imgs, HRSC_ND3_URLs_ODE, HRSC_ND3_URLs_ASU, HRSC_ND3_URLs_BER))
    glfJSON['HRSC_ND3'] = HRSC_tuples
                        
    # HRSC SR3 images
    HRSC_SR3imgs = HRSC_SR3_index.get(GLF['CatNum'], [])
    HRSC_SR3_URLs_ODE = []
    HRSC_SR3_URLs_ASU = []
    for himg in HRSC_SR3imgs:
        HRSC_URL_o = makeURL("o", himg)
        HRSC_URL_a = makeURL("a", himg)
        HRSC_SR3_URLs_ODE.append(HRSC_URL_o)
        HRSC_SR3_URLs_ASU.append(HRSC_URL_a)
    HRSC_tuples = list(zip(HRSC_SR3imgs, HRSC_SR3_URLs_ODE, HRSC_SR3_URLs_ASU))
    glfJSON['HRSC_SR3'] = HRSC_tuples    
    
    # HiRISE
    hiriseimgs = GLF['HiRISE_img'].split(',')
    hiriseimg2 = HiRISE_index.get(GLF['CatNum'], [])
    # remove excess whitespace
    hiriseimgs = [h.strip() for h in hiriseimgs]
    hiriseimg2 = [h.strip() for h in hiriseimg2]
    for himg in hiriseimg2:         
        if himg not in hiriseimgs and himg[:15] not in hiriseimgs and "COLOR" not in himg:
            hiriseimgs.append(himg)
    hiriseurls = []
    for himg in hiriseimgs:
        himg = himg.lstrip()
        hiriseurl = "http://hirise.lpl.arizona.edu/" + himg[:15]
        hiriseurls.append(hiriseurl)
    hiriseimgs = [h[:15] for h in hiriseimgs]
    hirise_tuples = list(zip(hiriseimgs, hiriseurls))
    glfJSON['HiRISE'] = hirise_tuples

    hiriseimgs_ext = HiRISE_ext_index.get(GLF['CatNum'], [])
    hiriseimgs_ext = [h[:15] for h in hiriseimgs_ext if "COLOR" not in h]
    hiriseurls2 = ["http://hirise.lpl.arizona.edu/"+h for h in hiriseimgs_ext]
    hirise_tuples2 = list(zip(hiriseimgs_ext, hiriseurls2))
    glfJSON['HiRISE_ext'] = hirise_tuples2
    
    # HiRISE anaglyphs
    anaglyphimgs = GLF['HiRISE_anaglyph'].split(',')
    hiriseanag2 = HiRISE_anaglyph_index.get(GLF['CatNum'], [])
    # remove excess whitespace
    anaglyphimgs = [h.strip() for h in anaglyphimgs]
    hiriseanag2 = [h.strip() for h in hiriseanag2]
     
    for aimg in hiriseanag2:
        if aimg not in anaglyphimgs:
            anaglyphimgs.append(aimg)
    anaglyphurls = []
    for aimg in anaglyphimgs:
        anaglyphurl = "http://hirise.lpl.arizona.edu/anaglyph/singula.php?ID="
        aimg = aimg.lstrip()
        leftobs = aimg[:15]
        anaglyphurl = anaglyphurl+leftobs
        anaglyphurls.append(anaglyphurl)
    anaglyph_tuples = list(zip(anaglyphimgs, anaglyphurls))
    glfJSON['anaglyph'] = anaglyph_tuples

    hiriseanags_ext = HiRISE_ext_anaglyph_index.get(GLF['CatNum'], [])
    anaglyphurls2 = ["http://hirise.lpl.arizona.edu/anaglyph/singula.php?ID="+h[:15] for h in hiriseanags_ext]
    anaglyph_tuples2 = list(zip(hiriseanags_ext, anaglyphurls2))
    glfJSON['anaglyph_ext'] = anaglyph_tuples2
    
    # HiRISE DTMs
    hiriseDTMs = GLF['HiRISE_DTM'].split(',')
    hiriseDTM2 = HiRISE_DTM_index.get(GLF['CatNum'], [])
    
    hiriseDTMs = [h.strip() for h in hiriseDTMs]
    hiriseDTM2 = [h.strip() for h in hiriseDTM2]
    for dimg in hiriseDTM2:
        if dimg not in hiriseDTMs:
            hiriseDTMs.append(dimg)
    DTMurls = []
    if hiriseDTMs == ['']:
        hiriseDTMs = []
    for dimg in hiriseDTMs:
        DTMurl = "http://www.uahirise.org/dtm/dtm.php?ID="
        # find the link to the HiRISE website
        dimg=dimg.lstrip()
        imgn = dimg[6:12]
        try:
            # if there is no DTM, skip over this code
            if int(imgn) >= 10000:
                dtm = dimg[:17].replace("DTEEC","ESP")
            else:
                dtm = dimg[:17].replace("DTEEC","PSP")
            DTMurl = DTMurl + dtm
        except:
            DTMurl = ''
        DTMurls.append(DTMurl)
    DTM_tuples = list(zip(hiriseDTMs, DTMurls))
    glfJSON['HiRISE_DTM'] = DTM_tuples
    glfJSON['Length'] = "{l:.2f} km".format(l=float(GLF['Length']))
    glfJSON['Width'] = "{w:.2f} km".format(w=float(GLF['Width']))
    glfJSON['Area'] = "{A:.2f} sq. km".format(A=float(GLF['Area']))
    glfJSON['Elevation'] = "{e:.0f}m".format(e=float(GLF['MeanElev']))
    glfJSON['Orientation'] = "{r:.2f} degrees".format(r=float(GLF['Orientation']))
    glfJSON['imagefile'] = "context_subsets/Souness{i:04d}_context2.png".format(i=int(GLF['CatNum']))
    glfJSON['DTMimagefile'] = "context_subsets/Souness{i:04d}DTM_context2.png".format(i=int(GLF['CatNum']))
    LyrFile = "context_subsets/Souness{i:04d}LyrStck_contextB132_str.png".format(i=int(GLF['CatNum']))
    if os.path.exists(LyrFile):
        glfJSON['LyrStackimagefile'] = LyrFile
    else:
        glfJSON['LyrStackimagefile'] = ""
    # DTM stats
    DTMstatsfile = "context_subsets/Souness{i:04d}DTM_context.txt".format(i=int(GLF['CatNum']))
    if os.path.exists(DTMstatsfile):
        glfJSON['DTMstats'] = readDTMStats(DTMstatsfile)
    else:
        glfJSON['DTMstats'] = {"Max":"","Min":"","stdDTM":"", "meanDTM":""}
    # nadir image dimensions
    NadirDims = "context_subsets/Souness{i:04d}_context.txt".format(i=int(GLF['CatNum']))
    if os.path.exists(NadirDims):
        glfJSON['NDdims'] = readNadirDims(NadirDims)
    else:
        glfJSON['NDdims'] = {"Width":"","Height":"", "PixelScale":""}
        
    # LnKHead stats
    # LnKHead stats file
    LnKHeadstatsfile = "context_subsets/Souness{i:04d}LnKhead.txt".format(i=int(GLF['CatNum']))
    if os.path.exists(LnKHeadstatsfile):
        glfJSON['LnKHeadstats'] = readLnKStats(LnKHeadstatsfile)
    else:
        glfJSON['LnKHeadstats'] = {"Max":"","Min":"","StdDev":"", "Mean":""}
    glfJSON['LnKHeadfile'] = "context_subsets/Souness{i:04d}LnKhead.png".format(i=int(GLF['CatNum']))
        
    glfJSON['ctxshapefile'] = "context_subsets/Souness{i:04d}_contextSHP2.png".format(i=int(GLF['CatNum']))
    glfJSON['extshapefile'] = "context_subsets/Souness{i:04d}_extentSHP2.png".format(i=int(GLF['CatNum']))
    #glfJSON['headshapefile'] = "context_subsets/Souness{i:04d}_headSHP.png".format(i=int(GLF['CatNum']))
    #glfJSON['termshapefile'] = "context_subsets/Souness{i:04d}_termSHP.png".format(i=int(GLF['CatNum']))
    #glfJSON['centshapefile'] = "context_subsets/Souness{i:04d}_centreSHP.png".format(i=int(GLF['CatNum']))
    #glfJSON['leftMCshapefile'] = "context_subsets/Souness{i:04d}_LMidCSHP.png".format(i=int(GLF['CatNum']))
    #glfJSON['rightMCshapefile'] = "context_subsets/Souness{i:04d}_RMidCSHP.png".format(i=int(GLF['CatNum']))
    glfJSON['pointsfile'] = "context_subsets/Souness{i:04d}_points.png".format(i=int(GLF['CatNum']))
    
    glfJSON['extallshapefile'] = "context_subsets/Souness{i:04d}_extentallSHP2.png".format(i=int(GLF['CatNum']))
    if len("".join(hiriseimgs)) > 0:
        #print(hiriseimgs)
        glfJSON['HiRISEfootfile'] =  "context_subsets/Souness{i:04d}_HiRISESHP.png".format(i=int(GLF['CatNum']))
    else:
        glfJSON['HiRISEfootfile'] =  ""
    if len("".join(anaglyphimgs)) > 0:
        #print(anaglyphimgs)
        glfJSON['HiRISEAfootfile'] =  "context_subsets/Souness{i:04d}_HiRISEASHP.png".format(i=int(GLF['CatNum']))
    else:
        glfJSON['HiRISEAfootfile'] =  ""
    
    profiles = glob.glob("ProfilePNGs/*Cat{i:04d}*.png".format(i=int(GLF['CatNum'])))
    profiles.sort()
    glfJSON['profilefiles'] = profiles
    
    # HTML to overplot on map of Mars
    backgroundimg =  "OverviewMap800px.png"
    markerHTML = "<div class='markercont' style='top: {t}px; left: {l}px;'><div id='diamond-narrow'></div></div>".format(bgr=backgroundimg,t=int(lat_to_top(float(GLF['Centlat']))), l=int(lng_to_left(float(GLF['Centlon180']))))
    backgroundHTML = "<div style='background-image: url({bgr}); height: 400px; width: 800px;'>"+markerHTML+"</div>"
    glfJSON['marsmapHTML'] = markerHTML
    return glfJSON

# read in files listing HiRISE images, anaglyphs and DTMs

#ctx9
HiRISE_index = {}
HiRISE_anaglyph_index = {}
HiRISE_DTM_index = {}

#ext
HiRISE_ext_index = {}
HiRISE_ext_anaglyph_index = {}
HiRISE_ext_DTM_index = {}

HRSC_ND3_index = {}
HRSC_SR3_index = {}

with open(HiRISE_CTX9) as csvfile:
    spamreader = csv.DictReader(csvfile, fieldnames=HiRISE_CTX9_headers,delimiter=',',quotechar='"')
    for row in spamreader:
        catnum, img = row['CatNum'], row['HiRISE_img']
        himglist = img.split(",")
        HiRISE_index[catnum] = himglist
with open(HiRISE_anaglyph_CTX9) as csvfile:
    spamreader = csv.DictReader(csvfile, fieldnames=HiRISE_CTX9_headers,delimiter=',',quotechar='"')
    for row in spamreader:
        catnum, img = row['CatNum'], row['HiRISE_img']
        himglist = img.split(",")
        HiRISE_anaglyph_index[catnum] = himglist

with open(HiRISE_EXT) as csvfile:
    spamreader = csv.DictReader(csvfile, fieldnames=HiRISE_CTX9_headers,delimiter=',',quotechar='"')
    for row in spamreader:
        catnum, img = row['CatNum'], row['HiRISE_img']
        himglist = img.split(",")
        HiRISE_ext_index[catnum] = himglist
with open(HiRISE_anaglyph_EXT) as csvfile:
    spamreader = csv.DictReader(csvfile, fieldnames=HiRISE_CTX9_headers,delimiter=',',quotechar='"')
    for row in spamreader:
        catnum, img = row['CatNum'], row['HiRISE_img']
        himglist = img.split(",")
        HiRISE_ext_anaglyph_index[catnum] = himglist
        
with open(HiRISE_DTM_CTX9) as csvfile:
    spamreader = csv.DictReader(csvfile, fieldnames=HiRISE_CTX9_headers,delimiter=',',quotechar='"')
    for row in spamreader:
        catnum, img = row['CatNum'], row['HiRISE_img']
        himglist = img.split(",")
        HiRISE_DTM_index[catnum] = himglist
        
with open(HiRISE_DTM_EXT) as csvfile:
    spamreader = csv.DictReader(csvfile, fieldnames=HiRISE_CTX9_headers,delimiter=',',quotechar='"')
    for row in spamreader:
        catnum, img = row['CatNum'], row['HiRISE_img']
        himglist = img.split(",")
        HiRISE_ext_DTM_index[catnum] = himglist
                
with open(HRSC_ND3) as csvfile:
    spamreader = csv.DictReader(csvfile, fieldnames=HRSC_ND3_EXT_headers,delimiter=',',quotechar='"')
    for row in spamreader:
        catnum, img = row['CatNum'], row['HRSC_img']
        himglist = img.split(",")
        HRSC_ND3_index[catnum] = himglist
with open(HRSC_SR3) as csvfile:
    spamreader = csv.DictReader(csvfile, fieldnames=HRSC_ND3_EXT_headers,delimiter=',',quotechar='"')
    for row in spamreader:
        catnum, img = row['CatNum'], row['HRSC_img']
        himglist = img.split(",")
        HRSC_SR3_index[catnum] = himglist
        
with open(Gfilein) as csvfile:
     # write the buttons for the index page
     writeHTMLbuttons(None, "sounessallbuttons.html", writeonly3D=False, allowCTX9=False)
     #input()
with open(Gfilein) as csvfile:
     writeHTMLbuttons(None, "souness_anaglyphbuttons.html", allowCTX9=False)
     #input()
with open(Gfilein) as csvfile:     
     writeHTMLbuttons(None, "souness_anaglyph_ctx9buttons.html", allowCTX9=True)
     #input()
with open(Gfilein) as csvfile:
     writeHTMLbuttons(None, "souness_DTMbuttons.html", writeonlyDTM=True, allowCTX9=False)
     #input()
with open(Gfilein) as csvfile:     
     writeHTMLbuttons(None, "souness_DTM_ctx9buttons.html", writeonlyDTM=True, allowCTX9=True)
     #input()     

# long+lat bounds for regions
# regions altered to make them non-overlapping
# and remove longitude gaps
#tharsis = [-180, -60, -70, -20]
tharsis = [-180, -70, -70, -20]
#argyre = [-75, 0, -70, -20]
argyre = [-70, 0, -70, -20]
whellas = [0, 75, -70, -20]
ehellas = [75, 120, -70, -20]
sehighland = [120, 180, -70, -20]
olympus = [-180, -100, 10, 70]
#mareotis = [-100, -60, 20, 70]
mareotis = [-100, -30, 20, 70]
#deuteron = [-15, 40, 20, 70]
deuteron = [-30, 40, 20, 70]
#proton = [35, 60, 20, 70]
proton = [40, 60, 20, 70]
#nilosyrtis = [60, 90, 20, 70]
nilosyrtis = [60, 100, 20, 70]
#utopiaphlegra = [110, 180, 20, 70]
utopiaphlegra = [100, 180, 20, 70]
npolar = [-180, 180, 70, 90]
spolar = [-180, 180, -90, -70]

regions = [tharsis, argyre, whellas, ehellas, sehighland, olympus, mareotis, deuteron, proton, nilosyrtis, utopiaphlegra, npolar, spolar]
regionnames = ["Tharsis", "Argyre", "West of Hellas", "East of Hellas", "SE Highlands", "Olympus Mons and surrounding area", "Mareotis Fossae", "Deuteronilus Mensae", "Protonilus Mensae", "Nilosyrtis Mensae", "Utopia Planitia and Phlegra Montes", "North Polar", "South Polar"]
regionURLs = ["stharsis.html", "argyre.html", "whellas.html", "ehellas.html", "sehighlands.html", "olympus.html", "mareotis.html",
              "deuteron.html", "proton.html", "nilosyrtis.html", "elysium.html", "npolar.html", "spolar.html"]

regions_outHTML = [r.replace(".html","list.html") for r in regionURLs]
regionURLs = ["http://taklowkernewek.neocities.org/mars/"+u for u in regionURLs]

regiondict = {key:value for (key, value) in zip(regionnames, regions)}
regionURLdict = {key:value for (key, value) in zip(regionnames, regionURLs)}


outFile_allHiRISEkw = "hirisekw_all.html"        

outFile_all = open(outFile_allHiRISEkw, "w")
outFile_all.write('\n<h3 id="hirisekw">Links to HiRISE images with Cornish titles</h3><p>As part of the <a href="http://www.uahirise.org/kw/">HiRISE Kernewek</a> website at the University of Arizona, the following HiRISE images have been described in Cornish. Some have red/blue 3D analgyphs which have not yet had Cornish titles added.</p>\n')        

for r,rn, rurl, h in zip(regions, regionnames, regionURLs, regions_outHTML):
    print(r)
    print('<h2 id="toptrumps">Links to individual pages on Souness GLFs in this region</h2>')
    with open(Gfilein) as csvfile:
        writeHTMLbuttons(r, h, writeonly3D=False)
        print('<h3 id="hirisekw">Links to HiRISE images with Cornish titles</h3>')
        print('<p>As part of the <a href="http://www.uahirise.org/kw/">HiRISE Kernewek</a> website at the University of Arizona, the following HiRISE images have been described in Cornish. Some have red/blue 3D analgyphs which have not yet had Cornish titles added.</p><p>See also a visual index at the <a href="https://www.uahirise.org/kw/catalog/">HiRISE Kernewek website</a>.</p>')
        hi_kw = printHiRISE_kw(r)
        outFile = open(h,"a")
        outFile.write('\n<h3 id="hirisekw">Links to HiRISE images with Cornish titles</h3><p>As part of the <a href="http://www.uahirise.org/kw/">HiRISE Kernewek</a> website at the University of Arizona, the following HiRISE images have been described in Cornish. Some have red/blue 3D analgyphs which have not yet had Cornish titles added.</p><p>See also a visual index at the <a href="https://www.uahirise.org/kw/catalog/" target="_blank">HiRISE Kernewek website</a>.</p>\n')
        outFile.write(hi_kw)
        outFile_all.write('<div class="taklowkwtextblock">\n')
        if "polar" not in rurl:
            outFile_all.write('<nav class="horiz horizMars"><ul><li><a href="{u}">{name}</a></li></ul></nav>\n'.format(name=rn, u=rurl))
        else:
            outFile_all.write('<h3>{name}</h3>\n'.format(name=rn))
        outFile_all.write('<h5>Longitude bounds {l1}, {l2}. Latitude bounds {l3}, {l4}.</h5>\n'.format(l1=r[0], l2=r[1], l3=r[2], l4=r[3]))
        outFile_all.write(hi_kw)
        outFile_all.write('</div>\n')

        
# start again for pages for each GLF
SounessJSON = {"Souness":{}}
SounessJSONFile = "souness_glf.json"
with open(Gfilein) as csvfile:
    spamreader = csv.DictReader(csvfile, fieldnames=fieldnames,delimiter=';',quotechar='"')
    for row in spamreader:
        print("Souness GLF top trumps")        
        print("Catalogue number {c}".format(c=row['CatNum']))        
        catnum = row['CatNum']
        Sindex[catnum] = row
        if catnum == "Catalogue number":
            pass
        else:
            # write the Top trump page
            #writeHTML(row)
            # write to JSON
            SounessJSON["Souness"][catnum] = createJSONObj(row)
"""            indshp = int(row['CatNum']) - 1     
            #print(indshp)
            shapefile = sounessGLFFilePath + CtxSHPsPath + 'context_' + str(indshp)+'.shp'
            # print shapefile
            print("Centre longitude: {l}\nCentre latitude: {t}".format(l=row['Centlon180'],t=row['Centlat']))
            if row['HRSC_DTM'] == 'none':
                print("Mars express DTM coverage {h}".format(h=row['HRSC_DTM']))
            else:
                print("Mars express DTM coverage {h}.\nDTM resolution {r}m".format(h=row['HRSC_DTM'],r=row['DTMres']))
                # get HRSC nadir image file and cut to CTX
                HRSC = row['HRSC_DTM']
                HRSC = HRSC[1:5]
                HRSCdir = HRSCPath + HRSC + '/'
                print(HRSCdir)
                os.chdir(HRSCdir)                
                nadirIMGFile = glob.glob('h'+HRSC+'*nd4*.kea')
                print(nadirIMGFile)                
                #for n in nadirIMGFile:
                #    makeImageFileCrop(n)                    
                os.chdir(sounessGLFFilePath) """
#print(SounessJSON)
with open(SounessJSONFile, "w") as outFile:
    SounessJSON = json.dump(SounessJSON, outFile, indent=None, sort_keys=True, separators=(',', ': '))
    

#while(True):
#    n = raw_input("Please enter your favourite Souness GLF (1-1309)?")
#    if int(n)>0 and int(n) < 1310:
#       print("Souness {n}".format(n=int(n)))
#       tuicmd = "tuiview Souness_{n}_CTX_6band.kea --rgb --bands 3,1,2 --stddev -v SounessROIs_individual/Individual/Extent/extent_{m}.shp".format(n=n,m=int(n)-1)
#       eogcmd = "eog Souness_{n}_CTX_nd4.png".format(n=n)
#       SounessObj = Sindex[n]
#       print("Latitude:{clat}\nLongitude:{clng}\nLength:{lth}\nWidth:{wth}\nArea:{A}\nHRSC:{H}".format(clat=SounessObj['Centlat'],clng=SounessObj['Centlon180'],
#                                                                                                        lth=SounessObj['Length'],wth=SounessObj['Width'],
#                                                                                                         A=SounessObj['Area'],H=SounessObj['HRSC_DTM']))
#       if SounessObj['HRSC_DTM'] != 'none':
#            print("HRSC DTM resolution: {r}m\nHiRISE_img: {i}\n,HIRiSE_anaglyph: {a}\n,HiRISE_DTM: {d}".format(r=SounessObj['DTMres'],i=SounessObj['HiRISE_img'],
#                                                                                                              a=SounessObj['HiRISE_anaglyph'],d=SounessObj['HiRISE_DTM']))
#            subprocess.call(tuicmd, shell=True)
#            subprocess.call(eogcmd, shell=True)
 
 
    
