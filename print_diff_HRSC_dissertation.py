# -*- coding: utf-8 -*-
import readallJSON
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

def print_tiles_notused(sounessGLFs, DTMres, HRSC_Souness, HRSC_DA4_GDALdict, quiet=True, html=False):
    tilenames = HRSC_DA4_GDALdict
    for t in DTMres:
        if t.lower() not in tilenames:
            sounessobjs = HRSC_Souness[t]
            dtm_res = DTMres[t]['resolution']
            prodID = DTMres[t]['prodID']
            prodURL = DTMres[t]['url']
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
                sounesslistitems = "".join(["<span><a href='{sURL}' target'_blank'>{s}</a> </span>".format(sURL=toptrumpURL(s),
                                                                                                           s=s) for s in sounessobjs])
                print("<h4>Tile {t}</h4><dl><dt>Resolution:</dt><dd>{r}m</dd><dt>Product ID:</dt><dd><a href='{b}' target='_blank'>{p}</a></dd><dt>Souness GLFs:</dt><dd>{GLFs}</dd></dl>".format(t=t, r=dtm_res, p=prodID, b=prodURL, GLFs=sounesslistitems))
            else:
                print("Tile {t}: Resolution {r}m.\nProduct ID: {p}. URL: {b}\nSouness objects: {s}".format(t=t,
                                                                                                         r=dtm_res,
                                                                                                         p=prodID,
                                                                                                         b=prodURL,
                                                                                                         s=" ".join(sounessobjs)))
            if html:
                startp = "<p>"
                endp = "</p>"
            else:
                startp = ""
                endp = ""
            if bestresused:                
                print("{sp}Best available resolution used for all Souness objects in this tile{ep}".format(sp=startp, ep=endp))
            if not(bestresused and quiet):
                print("{sp}In dissertation, following HRSC DTM tiles used:{ep}".format(sp=startp, ep=endp))
                if html: print("<dl>")
                for s in sounessobjs:
                    tileused = sounessGLFs[str(s)]["HRSC_DTM"]
                    if "HRSC_DTM_res" in sounessGLFs[str(s)]:
                        tileres = sounessGLFs[str(s)]["HRSC_DTM_res"]
                    else:
                        tileres = "none "
                    if html:
                        print("<dt><a href='{sURL}' target='_blank'>Souness {s}</a></dt><dd><a href='{b}' target='_blank'>{t}</a>, resolution {r}m</dd>".format(sURL=toptrumpURL(s), s=s, t=tileused, r=tileres, b=berlinURL(tileused)))
                    else:
                        print("S{s}: {t}, resolution {r}m.".format(s=s,
                                                                   t=tileused,
                                                                   r=tileres))
            if html:
                print("</dl><p>{n}</p><br>".format(n=notfound))
            else:
                print("{n}\n".format(n=notfound))

DTMres = readallJSON.DTMres
HRSC_da4dict = readallJSON.HRSC_da4dict
sounessGLFs = readallJSON.sounessGLFs
HRSC_Souness = readallJSON.HRSC_Souness
print_tiles_notused(sounessGLFs, DTMres, HRSC_Souness, HRSC_da4dict, quiet=True, html=True)


    
