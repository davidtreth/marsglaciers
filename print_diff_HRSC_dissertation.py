# -*- coding: utf-8 -*-
import readallJSON
import numpy
"""
This program compares the list of HRSC tiles used in the dissertation work with the one from intersecting the HRSC DTM footprints with Souness extents.
"""

def berlinURL(prodID):
    if prodID == "none":
        return ""
    else:
        return "http://hrscview.fu-berlin.de/cgi-bin/ion-p?page=product2.ion&code=&image={i}".format(i=prodID[1:10].lower())
def toptrumpURL(sounessNum):
    return "https://taklowkernewek.neocities.org/mars/sounesstoptrumps_js.html?S{s}".format(s=sounessNum)

def orbitlocationMap(lat, lng):
    return "http://maps.planet.fu-berlin.de/?zoom=7&lat={lat:.5f}&lon={lng:.5f}&layers=B0FFFTTT".format(lat=lat, lng=lng)
    
def makelink(url, contenta):
    return "<a href='{url}' target='_blank'>{c}</a>".format(url=url, c=contenta)

def getCentre(HRSCda4_dictval):
    latlng_coords =  [HRSCda4_dictval['wgs84Extent']['coordinates'][0]]
    """
    upperLefts = latlng_coords[0]
    upperRights = latlng_coords[2]
    lowerLefts = latlng_coords[1]
    lowerRights = latlng_coords[3]
    """
    #print(latlng_coords)
    #print([x[0] for x in latlng_coords[0][:4]])
    #print([x[1] for x in latlng_coords[0][:4]])
    centreLng = numpy.mean([x[0] for x in latlng_coords[0][:4]])
    centreLat = numpy.mean([x[1] for x in latlng_coords[0][:4]])
    return centreLat, centreLng
def print_tiles_notused(sounessGLFs, DTMres, HRSC_Souness, HRSC_DA4_GDALdict, HRSC_DTM_coverage, quiet=True, html=False):
    if html:
        startp = "<p>"
        endp = "</p>"
    else:
        startp = ""
        endp = ""
    # tiles used in dissertation
        
    tilenames = HRSC_DA4_GDALdict
    if html:
        print("<h3>HRSC DTM tiles intersecting Souness Glacier like forms but not used in the {d}. {t}</h3>".format(d=makelink("http://taklowkernewek.neocities.org/dissertation_final_reducedsize.pdf", "dissertation"), t=makelink("http://taklowkernewek.neocities.org/dissertation_tablet_smallerfilesize.pdf", "Tablet version")))
    else:
        print("HRSC DTM tiles intersecting Souness Glacier like forms but not used in the dissertation")
    print("{sp}Total DTM tiles in dissertation = {d}, total tiles intersecting GLF extents = {a}.{ep}".format(d=len(tilenames),
          a=len(DTMres), sp=startp, ep=endp))
    diffn = len([t for t in DTMres if t.lower() not in tilenames])
    diffn2 = len([t for t in tilenames if t.upper() not in DTMres])
    print("{sp}Tiles intersection not used in dissertation = {d1}. Tiles in dissertation that do not intersect = {d2}.{ep}".format(sp=startp, ep=endp, d1 = diffn, d2 = diffn2))
    DTMtiles_intersect = sorted(list(DTMres))
    for t in DTMtiles_intersect:
        if t.lower() not in tilenames:
            sounessobjs = HRSC_Souness[t]
            dtm_res = DTMres[t]['resolution']
            prodID = DTMres[t]['prodID'][:10]
            prodURL = DTMres[t]['url']
            prodCenLat = float(HRSC_DTM_coverage[prodID]["CenterLat"])
            prodCenLon = float(HRSC_DTM_coverage[prodID]["CenterLon"])
            # in the coverage shapefile, longitude was in the 0 to 360 deg system
            if prodCenLon > 180:
                prodCenLon -= 360
            prodMap = orbitlocationMap(prodCenLat, prodCenLon)
            notfound = "none"
            
            maxpixelsize = 0            
            for s in sounessobjs:
                # loop through the souness objects in the field once so that 
                if "HRSC_DTM_res" in sounessGLFs[str(s)]:
                    notfound = ""
                    if float(sounessGLFs[str(s)]["HRSC_DTM_res"]) > maxpixelsize:
                        maxpixelsize = float(sounessGLFs[str(s)]["HRSC_DTM_res"])
                else:
                    maxpixelsize = 500
                        
            bestresused = (dtm_res >= maxpixelsize)
            if html:
                sounesslistitems = "".join(["<span><a href='{sURL}' target='_blank'>{s}</a> </span>".format(sURL=toptrumpURL(s),
                                                                                                           s=s) for s in sounessobjs])
                                                                                                           
                #print("<h4>Tile {t}</h4><dl><dt>Resolution:</dt><dd>{r}m</dd><dt>Product ID:</dt><dd><a href='{b}' target='_blank'>{p}</a> {maplink}</dd><dt>Centre location:</dt><dd>Lat: {lt:.2f}°, Long:{lg:.2f}°.</dd><dt>Souness GLFs:</dt><dd>{GLFs}</dd></dl>".format(t=t, r=dtm_res, p=prodID, b=prodURL, GLFs=sounesslistitems)
                print("<div class='hrsctile'><h4>HRSC tile {t}</h4><table class='newtiletable'><tr><th>Resolution (m)</th><th>Product ID</th><th>Centre location</th><th>Souness GLFs</th></tr><tr><td>{r:.0f}</td><td><a href='{b}' target='_blank'>{p}</a> {maplink}</td><td>Lat: {lt:.1f}°, Long: {lg:.1f}°</td><td>{GLFs}</td></tr></table>".format(t=t, r=float(dtm_res), p=prodID, b=prodURL, maplink=makelink(prodMap, "show on map"), GLFs=sounesslistitems, lt=float(prodCenLat), lg=float(prodCenLon)))
            else:
                print("Tile {t}: Resolution {r}m.\nProduct ID: {p}. URL: {b}\nSouness objects: {s}".format(t=t,
                                                                                                         r=dtm_res,
                                                                                                         p=prodID,
                                                                                                         b=prodURL,
                                                                                                         s=" ".join(sounessobjs)))

            if bestresused:                
                print("{sp}Best available resolution used for all Souness objects in this tile{ep}".format(sp=startp, ep=endp))
            else:
                print("{sp}A better resolution may have been available for one or more Souness objects in this tile{ep}".format(sp=startp.replace("<p>","<p><strong>"), ep=endp.replace("</p>","</strong></p>")))
            if not(bestresused and quiet):                
                print("{sp}In the  dissertation, the following HRSC DTM tiles were used:{ep}".format(sp=startp, ep=endp))
                if html: 
                    print("<table class='dissertable'><tr><th>Souness GLF</th><th>Product ID</th><th>Resolution (m)</th><th>Centre location</th></tr>")
                    #print("<dl>")
                for s in sounessobjs:
                    tileused = sounessGLFs[str(s)]["HRSC_DTM"][:-4]
                    tile5 = tileused[:5]
                    tile5 = tile5.lower()
                    if tile5 == "":
                        prodCen = sounessGLFs[str(s)]["Centlat"], sounessGLFs[str(s)]["Centlon"]
                    else:
                        prodCen = getCentre(tilenames[tile5])
                    prodMap = orbitlocationMap(prodCen[0], prodCen[1])
                    if "HRSC_DTM_res" in sounessGLFs[str(s)]:
                        tileres = sounessGLFs[str(s)]["HRSC_DTM_res"]
                    else:
                        tileres = "none "
                    if html:
                        #print("<dt><a href='{sURL}' target='_blank'>Souness {s}</a></dt><dd><a href='{b}' target='_blank'>{t}</a> {maplink}, resolution {r}m. Centre location:</dt><dd>Lat: {lt:.2f}°, Long: {lg:.2f}°.</dd>".format(sURL=toptrumpURL(s), s=s, t=tileused, r=tileres, b=berlinURL(tileused), maplink=makelink(prodMap, "show on map"), lt=prodCen[0], lg=prodCen[1]))
                        print("<tr><td><a href='{sURL}' target='_blank'>{s}</a></td><td><a href='{b}' target='_blank'>{t}</a> {maplink}</td><td>{r}</td><td>Lat: {lt:.1f}°, Long: {lg:.1f}°</td></tr>".format(sURL=toptrumpURL(s), s=s, t=tileused, r=tileres, b=berlinURL(tileused), maplink=makelink(prodMap, "show on map"), lt=prodCen[0], lg=prodCen[1]))
                    else:
                        print("S{s}: {t}, resolution {r}m.".format(s=s,
                                                                   t=tileused,
                                                                   r=tileres))
            if html:
                print("</table></div>")
                #print("</dl><p>{n}</p><br>".format(n=notfound))
            else:
                print("{n}\n".format(n=notfound))

DTMres = readallJSON.DTMres
HRSC_da4dict = readallJSON.HRSC_da4dict
sounessGLFs = readallJSON.sounessGLFs
HRSC_Souness = readallJSON.HRSC_Souness
HRSC_DTM_coverage = readallJSON.HRSC_DTM_coverage
print_tiles_notused(sounessGLFs, DTMres, HRSC_Souness, HRSC_da4dict, HRSC_DTM_coverage, quiet=False, html=True)
#h0037cen = getCentre(HRSC_da4dict['h0037'])
#print(orbitlocationMap(h0037cen[0], h0037cen[1]))
    
