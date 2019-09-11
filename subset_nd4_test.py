# create subsets of the nadir image, and rasterized shapefiles
# for the Souness GLFs that have HRSC DTM data
# also create DTM image
# and layerstacked HRSC image and DTM and slope
# crop the nadir image to the bounding box of the context shapefile of each Souness GLF
# and make rasterized images from context, extent, and head shapefiles
# for overplotting on the nd image files for example
# where there is no HRSC coverage, use MGS MOC and MOLA data
import rsgislib
from rsgislib import imageutils, vectorutils, imagecalc
from rsgislib.imagecalc import BandDefn
import subprocess
import csv
import os
import os.path
import glob

# file paths hard-coded
sounessGLFFilePath = "/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/"
sounessGLFFile="mmc1_HRSC+HiRISE_coverage_duplicates_possible_typos.csv"
inND4path =  '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessCatalog3_backup/'
outND4path = 'context_subsets/'

inMOCFile = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/MOLA_128/MOC_wideangle_mosaic_64/lat0_40/msss_atlas.kea'
inMOLAFile = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/MOLA_128/MOLA_128_eqc_lat0_40.kea'
inMOLALyrSt_N = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/MOLA_128/MOLA_128_NmidlataspectN.kea'
inMOLALyrSt_S = '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/MOLA_128/MOLA_128_SmidlataspectN.kea'

# locations of Souness GLF individual shapefiles
contextpath = 'SounessROIs_individual/Individual/Context/'
extentpath = 'SounessROIs_individual/Individual/Extent/'
headpath = 'SounessROIs_individual/Individual/heads/'

# location of all Souness extents shapefile

extent_allpath = 'SounessROIs/'
extent_allfile = 'SounessROIextents_all_Mars2000EqCyl_lat0_40.shp'
extent_all = extent_allpath + extent_allfile

heads_allfile = 'SounessROIheads_all_Mars2000EqCyl_lat0_40.shp' 
centres_allfile = 'SounessROIcentres_all_Mars2000EqCyl_lat0_40.shp' 
termini_allfile = 'SounessROItermini_all_Mars2000EqCyl_lat0_40.shp'
midchL_allfile = 'SounessROIleftmidchannel_all_Mars2000EqCyl_lat0_40.shp'
midchR_allfile = 'SounessROIrightmidchannel_all_Mars2000EqCyl_lat0_40.shp'

heads_all = extent_allpath + heads_allfile 
centres_all = extent_allpath + centres_allfile 
termini_all = extent_allpath + termini_allfile
midchL_all = extent_allpath + midchL_allfile
midchR_all = extent_allpath + midchR_allfile

Gfilein = sounessGLFFilePath+sounessGLFFile
print(Gfilein)

# HiRiSE footprints file (in equicylindrical coordinate system with standard paralell 40°
footprpath = 'hirisecoverage/eqcyl40/'
HiRISE_foot = 'mars_mro_hirise_rdrv11_eqcyl40.shp'
HiRISE_anag = 'mars_mro_hirise_anagly_eqcyl40.shp'
HiRISE_dtm = 'mars_mro_hirise_dtm_eqcyl40.shp'
Hfilein = footprpath + HiRISE_foot
HAfilein =footprpath + HiRISE_anag

fieldnames=['CatNum','CTXimg','Typo','offcent','Duplicate','HRSC_DTM','DTMres','HiRISE',
            'HiRISE_img','HiRISE_anaglyph','HiRISE_DTM','Hemisph','Headlon','Region','Region2',
            'Headlon180','Headlat','Termlon','Termlon180','Termlat','MidchRlon',
            'MidchRlon180','MidchRlat','MidchLlon','MidchLlon180','MidchLlat',
            'Centlon','Centlon180','Centlat','Length','Width','Area','Orientation',
            'MinElev','MaxElev','MeanElev','StdElev','Elongation','Midchlon',
            'Midchlat','distMidCCent','chanwidth','ratiooffset']

# list of Souness objects to use Mars Global Surveyor data instead
# these are areas where the context bbox falls in a nodata area
CatNumsForceMGS = []#[206, 228, 231, 262, 687, 688, 912, 1153]


# read in files listing HiRISE images, anaglyphs and DTMs
#ctx9
HiRISE_index = {}
HiRISE_anaglyph_index = {}
#HiRISE_CTX9 = 'SounessROIs/hirise_ctx9.csv'
HiRISE_CTX9 = 'SounessROIs/souness_context9_HiRISEimg_tiles.csv'
#HiRISE_anaglyph_CTX9 = 'SounessROIs/hirise_anaglyph_ctx9.csv'
HiRISE_anaglyph_CTX9 = 'SounessROIs/souness_context9_HiRISEana_tiles.csv'
HiRISE_CTX9_headers = ['CatNum', 'HiRISE_img', 'ContainsArr']
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

with open(Gfilein) as csvfile:
        spamreader = csv.DictReader(csvfile, fieldnames=fieldnames,delimiter=';',quotechar='"')
        for row in spamreader:
            print("Souness GLF top trumps")
            catnum = row['CatNum']
            print("Catalogue number {c}".format(c=catnum))
            if catnum == "Catalogue number":
                pass
            else:
                print("HRSC_DTM: {d}".format(d=row['HRSC_DTM']))
                HRSC_DTMfile = row['HRSC_DTM'].lower()
                      
                if True:
                      if HRSC_DTMfile == 'none' or int(catnum) in CatNumsForceMGS:
                        MGSmode = True
                      else:
                        MGSmode = False
                      HRSCdir = HRSC_DTMfile[1:5]
                      if MGSmode:
                        inND4 = inMOCFile
                      else:
                        nd4file = glob.glob(inND4path+HRSCdir+'/'+HRSC_DTMfile[:5]+'*nd4_Mars2000EqCyl_lat0_40.kea')
                        print(nd4file[0])
                        inND4 = nd4file[0]
                      outND4 = outND4path + "Souness{c:04d}_context.tif".format(c=int(catnum))
                      # stretched
                      outND4_s = outND4path + "Souness{c:04d}_context2.tif".format(c=int(catnum))

                      # image dimensions
                      statsND = outND4path + "Souness{c:04d}_context.txt".format(c=int(catnum))
                      if MGSmode:
                        inDTM = inMOLAFile
                      else:
                        DTMfile = glob.glob(inND4path+HRSCdir+'/LandSerf/'+HRSC_DTMfile[:5]+'*rawAsp.kea')
                        print(DTMfile[0])
                        inDTM = DTMfile[0]
                        DTMband = inDTM.replace(".kea", "_DTM.tif")
                      outDTM = outND4path + "Souness{c:04d}DTM_context.tif".format(c=int(catnum))
                      if not(MGSmode):
                        # LnK head vector polygons
                        vecpolysfiles = glob.glob(inND4path+HRSCdir+'/LandSerf/rsgis_02sqkm/*isectCtx9_joined.shp')
                        print(vecpolysfiles[0])
                        inVecPolys = vecpolysfiles[0]
                        rastVecPolysLnK = outND4path + "Souness{c:04d}LnKhead.tif".format(c=int(catnum))
                        rastVecPolysLnK_a = outND4path + "Souness{c:04d}LnKhead1.tif".format(c=int(catnum))
                        rastVecPolysLnK_s = outND4path + "Souness{c:04d}LnKhead2.tif".format(c=int(catnum))
                        statsLnKHead = outND4path + "Souness{c:04d}LnKhead.txt".format(c=int(catnum))
                      
                        # layerstack file
                        # use same layerstack as DTM for now
                        inLayerstackFile = glob.glob(inND4path+HRSCdir+'/LandSerf/'+HRSC_DTMfile[:5]+'*_rawAsp_add9999_6band.kea')
                        inLyrSt = inLayerstackFile[0]
                        outLyrSt = outND4path + "Souness{c:04d}LyrStck_context.kea".format(c=int(catnum))
                        outLyrSt2 = outND4path + "Souness{c:04d}LyrStck_contextB132.kea".format(c=int(catnum))
                        # stretched
                        outLyrSt_s = outND4path + "Souness{c:04d}LyrStck_contextB132_str.kea".format(c=int(catnum))                                                                                                                                                     
                      # stretched
                      outDTM_a = outND4path + "Souness{c:04d}DTM_context1.tif".format(c=int(catnum))
                      outDTM_s = outND4path + "Souness{c:04d}DTM_context2.tif".format(c=int(catnum))
                      statsDTM = outND4path + "Souness{c:04d}DTM_context.txt".format(c=int(catnum))
                      
                      # context
                      outCTXrast = outND4path + "Souness{c:04d}_contextSHP.tif".format(c=int(catnum))
                      outCTXrast_s = outND4path + "Souness{c:04d}_contextSHP2.tif".format(c=int(catnum))
                      # extent
                      outEXTrast = outND4path + "Souness{c:04d}_extentSHP.tif".format(c=int(catnum))
                      outEXTrast_s = outND4path + "Souness{c:04d}_extentSHP2.tif".format(c=int(catnum))
                      # head
                      outHeadrast = outND4path + "Souness{c:04d}_headSHP.tif".format(c=int(catnum))
                      outHeadrast_s = outND4path + "Souness{c:04d}_headSHP2.tif".format(c=int(catnum))
                      # centre
                      outCentrast = outND4path + "Souness{c:04d}_centreSHP.tif".format(c=int(catnum))
                      outCentrast_s = outND4path + "Souness{c:04d}_centreSHP2.tif".format(c=int(catnum))
                      # terminus
                      outTermrast = outND4path + "Souness{c:04d}_termSHP.tif".format(c=int(catnum))
                      outTermrast_s = outND4path + "Souness{c:04d}_termSHP2.tif".format(c=int(catnum))
                      # leftmidch
                      outLMidCrast = outND4path + "Souness{c:04d}_LMidCSHP.tif".format(c=int(catnum))
                      outLMidCrast_s = outND4path + "Souness{c:04d}_LMidCSHP2.tif".format(c=int(catnum))
                      # rightmidch
                      outRMidCrast = outND4path + "Souness{c:04d}_RMidCSHP.tif".format(c=int(catnum))
                      outRMidCrast_s = outND4path + "Souness{c:04d}_RMidCSHP2.tif".format(c=int(catnum))

                      # extents_all
                      outEXTALLrast = outND4path + "Souness{c:04d}_extentallSHP.tif".format(c=int(catnum))
                      outEXTALLrast_s = outND4path + "Souness{c:04d}_extentallSHP2.tif".format(c=int(catnum))
                      # HiRISE footprints
                      outHiRISErast = outND4path + "Souness{c:04d}_HiRISESHP.tif".format(c=int(catnum))
                      outHiRISErast_s = outND4path + "Souness{c:04d}_HiRISESHP2.tif".format(c=int(catnum))
                      outHiRISEArast = outND4path + "Souness{c:04d}_HiRISEASHP.tif".format(c=int(catnum))
                      outHiRISEArast_s = outND4path + "Souness{c:04d}_HiRISEASHP2.tif".format(c=int(catnum))                     

                      # points composite
                      outPoints = outND4path + "Souness{c:04d}_points.png".format(c=int(catnum))
                      
                      contextvect = '{p}context_{c}.shp'.format(p=contextpath, c=int(catnum)-1)
                      extentvect = '{p}extent_{c}.shp'.format(p=extentpath, c=int(catnum)-1)
                      # these ones start at 1 rather than 0!
                      headvect =  '{p}SounessROIheads_all_Mars2000EqCyl_lat0_40_OBJ_ID__{c}.shp'.format(p = headpath, c=int(catnum))
                      try:
                        # if possible, work in rsgislib but fall back on gdalwarp if needed
                        imageutils.subset(inND4,contextvect,outND4,'GTiff',rsgislib.TYPE_8INT)
                      except:
                        input("imageutils.subset not working")
                        gdwarpcmd = "gdalwarp -cutline {c} -crop_to_cutline {i} {out}".format(c=contextvect, i=inND4.replace("TOSHIBA EXT", "TOSHIBA\ EXT"), out=outND4)
                        print(gdwarpcmd)
                        subprocess.call(gdwarpcmd, shell=True)
                      if not(MGSmode):
                        try:
                           # if possible, work in rsgislib but fall back on gdalwarp if needed
                           if not(os.path.isfile(DTMband)):
                              imageutils.selectImageBands(inDTM, DTMband, 'GTiff', rsgislib.TYPE_32FLOAT, [2])
                           imageutils.subset(DTMband,contextvect,outDTM,'GTiff',rsgislib.TYPE_32FLOAT)
                        except:
                           input("imageutils.selectImageBands or imageutils.subset not working")
                           gdwarpcmd = "gdalwarp -cutline {c} -crop_to_cutline {i} {out}".format(c=contextvect, i=DTMband.replace("TOSHIBA EXT", "TOSHIBA\ EXT"), out=outDTM)
                           print(gdwarpcmd)
                           subprocess.call(gdwarpcmd, shell=True)
                      else:
                         try:
                            # if possible, work in rsgislib but fall back on gdalwarp if needed
                            imageutils.subset(inMOLAFile,contextvect,outDTM,'GTiff',rsgislib.TYPE_32FLOAT)
                         except:
                            gdwarpcmd = "gdalwarp -cutline {c} -crop_to_cutline {i} {out}".format(c=contextvect, i=inMOLAFile.replace("TOSHIBA EXT", "TOSHIBA\ EXT"), out=outDTM)
                            print(gdwarpcmd)
                            subprocess.call(gdwarpcmd, shell=True)

                      if not(MGSmode):
                        skipLyrSt = False
                        try:
                           imageutils.subset(inLyrSt, contextvect, outLyrSt, 'KEA', rsgislib.TYPE_32FLOAT)
                           imageutils.selectImageBands(outLyrSt, outLyrSt2, 'KEA', rsgislib.TYPE_32FLOAT, [1, 3, 2])
                           imageutils.popImageStats(outLyrSt, True, 0, True)
                           imageutils.popImageStats(outLyrSt2, True, 0, True)
                        except:                        
                           input("subset not working")
                           gdwarpcmd = "gdalwarp -of KEA -cutline {c} -crop_to_cutline {i} {out}".format(c=contextvect, i=inLyrSt.replace("TOSHIBA EXT", "TOSHIBA\ EXT"), out=outLyrSt)
                           print(gdwarpcmd)
                           subprocess.call(gdwarpcmd, shell=True)
                           skipLyrSt = True
                      else:
                        skipLyrSt = True

                      # I had some problems with this so used gdal_rasterize
                      #vectorutils.rasterise2Image(contextvect,outND4, outCTXrast, 'GTiff', 'FID')
                      # retrieve the nadir image file pixel scale and extents
                      gdalinf = subprocess.check_output("gdalinfo {i}".format(i= outND4),shell=True)
                      gdalinf = gdalinf.decode("utf-8")
                      print(gdalinf)

                      x, y = 12.5, -12.5
                      for line in str(gdalinf).split("\n"):
                              if line[:10] == "Pixel Size":
                                      xy = line.split("(")[1]
                                      xy = xy.split(")")[0]
                                      x, y = xy.split(",")
                              if line[:10] == "Lower Left":
                                      xmin_ymin = line.split("(")[1]
                                      xmin_ymin = xmin_ymin.split(")")[0]
                                      xmin, ymin = xmin_ymin.split(",")                                      
                              if line[:11] == "Upper Right":
                                      xmax_ymax = line.split("(")[1]
                                      xmax_ymax = xmax_ymax.split(")")[0]
                                      xmax, ymax = xmax_ymax.split(",")
                      xmin = xmin.strip()
                      ymin = ymin.strip()
                      xmax = xmax.strip()
                      ymax = ymax.strip()
                                                                                        
                      imgwidth = int(float(xmax) - float(xmin))
                      imgheight = int(float(ymax) - float(ymin))
                      with open(statsND, "w") as outF:
                        outF.write("Width,Height, PixelScale\n")
                        outF.write("{w},{h},{psize}".format(w=imgwidth, h=imgheight,psize=x))
                      
                      print(x,y)
                      print(imgwidth,imgheight)
                      if not(MGSmode):
                        DTMres = float(row['DTMres'])
                        scalefactor = DTMres / float(x)
                        print("DTM resolution is {d}, scalefactor = {s}".format(d=DTMres, s=scalefactor))
                      else:
                        scalefactor = 1.8331153488468312    
                      
                      # rasterize the shapefile
                      #gdalrastcmd = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -tr {x} {y} {vc} {vcrst}".format(x=x, y=y, vc = contextvect, vcrst = outCTXrast)                                          
                      gdalrastcmd = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = extentvect, vcrst = outEXTrast)
                      print(gdalrastcmd)
                      subprocess.call(gdalrastcmd, shell=True)
                      #head
                      gdalrastcmdH = 'gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -where "OBJ_ID=\'{cnum}\'" -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}'.format(cnum = catnum, xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = heads_all, vcrst = outHeadrast)
                      print(gdalrastcmdH)
                      subprocess.call(gdalrastcmdH, shell=True)
                      #centre
                      gdalrastcmdC = 'gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -where "OBJ_ID=\'{cnum}\'" -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}'.format(cnum = catnum, xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = centres_all, vcrst = outCentrast)
                      print(gdalrastcmdC)
                      subprocess.call(gdalrastcmdC, shell=True)
                      #terminus
                      gdalrastcmdT = 'gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -where "OBJ_ID=\'{cnum}\'" -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}'.format(cnum = catnum, xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = termini_all, vcrst = outTermrast)
                      print(gdalrastcmdT)
                      subprocess.call(gdalrastcmdT, shell=True)
                      #leftMid
                      gdalrastcmdL = 'gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -where "OBJ_ID=\'{cnum}\'" -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}'.format(cnum = catnum, xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = midchL_all, vcrst = outLMidCrast)
                      print(gdalrastcmdL)
                      subprocess.call(gdalrastcmdL, shell=True)
                      #rightMid
                      gdalrastcmdR = 'gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -where "OBJ_ID=\'{cnum}\'" -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}'.format(cnum = catnum, xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = midchR_all, vcrst = outRMidCrast)
                      print(gdalrastcmdR)
                      subprocess.call(gdalrastcmdR, shell=True)

                      gdalrastcmd2 = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = extent_all, vcrst = outEXTALLrast)
                      print(gdalrastcmd2)
                      subprocess.call(gdalrastcmd2, shell=True)

                      gdalrastcmd_vpoly = "gdal_rasterize -a LnKHead -of GTiff -init -20 -a_nodata -20 -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} '{vc}' {vcrst}".format(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax, x=x, y=y, vc = inVecPolys, vcrst = rastVecPolysLnK)
                      print(gdalrastcmd_vpoly)
                      subprocess.call(gdalrastcmd_vpoly, shell=True)
                      if catnum in HiRISE_index:
                              gdalrastcmd_Hi = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = Hfilein, vcrst = outHiRISErast)
                              print(gdalrastcmd_Hi)
                              subprocess.call(gdalrastcmd_Hi, shell=True)
                      if catnum in HiRISE_anaglyph_index:
                              gdalrastcmd_HiA = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = HAfilein, vcrst = outHiRISEArast)
                              print(gdalrastcmd_HiA)
                              subprocess.call(gdalrastcmd_HiA, shell=True)
                      
                      # stretch image to byte 8-bit by linear MinMax
                      imageutils.stretchImage(outND4,outND4_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      
                      # do the same for DTMs

                      datatype=rsgislib.TYPE_32FLOAT
                      expression = 'b1+9999'
                      bandDefns = []
                      bandDefns.append(BandDefn('b1', outDTM, 1))

                      
                      imagecalc.bandMath(outDTM_a, expression, 'GTiff', datatype, bandDefns)
                      imagecalc.imageStats(outDTM_a, statsDTM, True)



                      if not(MGSmode):
                        # LnK
                        datatype=rsgislib.TYPE_32FLOAT
                        minLnKH = 12.0
                        expression = 'max(b1, {m}) - {m}'.format(m=minLnKH)
                        bandDefns = []
                        bandDefns.append(BandDefn('b1', rastVecPolysLnK, 1))
                        imagecalc.bandMath(rastVecPolysLnK_a, expression, 'GTiff', datatype, bandDefns)
                        imagecalc.imageStats(rastVecPolysLnK_a, statsLnKHead, True)
                      
                      imageutils.stretchImage(outDTM_a,outDTM_s,False,'',True,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      if not skipLyrSt:
                        imageutils.stretchImage(outLyrSt2,outLyrSt_s,False,'',True,True,'KEA',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      # do the same for shapefile rasters (though may be unnecessary)
                      #imageutils.stretchImage(outCTXrast,outCTXrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outEXTrast,outEXTrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outHeadrast,outHeadrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outCentrast,outCentrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outTermrast,outTermrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outLMidCrast,outLMidCrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outRMidCrast,outRMidCrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outEXTALLrast,outEXTALLrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)

                      # don't do stretch step for HiRISE and HiRISE anaglyph - was unnecessary and avoids problem when HiRISE contains bounding box of ctx
                      #if catnum in HiRISE_index:
                      #        imageutils.stretchImage(outHiRISErast,outHiRISErast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      #if catnum in HiRISE_anaglyph_index:
                      #        imageutils.stretchImage(outHiRISEArast,outHiRISEArast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      if not(MGSmode):
                        imageutils.stretchImage(rastVecPolysLnK_a,rastVecPolysLnK_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)

                      # make png files
                      gdaltranscmd1 = "gdal_translate -of PNG  {c} {cP}".format(c=outND4_s,cP = outND4_s.replace(".tif",".png"))
                      # the nodata value makes the area outside the shapefile transparent
                      #gdaltranscmd2 = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outCTXrast_s,cP = outCTXrast_s.replace(".tif",".png"))
                      gdaltranscmd2 = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outEXTrast_s,cP = outEXTrast_s.replace(".tif",".png"))
                      gdaltranscmd2H = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outHeadrast_s,cP = outHeadrast_s.replace(".tif",".png"))
                      gdaltranscmd2C = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outCentrast_s,cP = outCentrast_s.replace(".tif",".png"))
                      gdaltranscmd2T = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outTermrast_s,cP = outTermrast_s.replace(".tif",".png"))
                      gdaltranscmd2L = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outLMidCrast_s,cP = outLMidCrast_s.replace(".tif",".png"))
                      gdaltranscmd2R = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outRMidCrast_s,cP = outRMidCrast_s.replace(".tif",".png"))

                      convertH = "convert {i} +level-colors black,red {o}".format(i=outHeadrast_s.replace(".tif",".png"), o=outHeadrast_s.replace("2.tif",".png"))
                      convertC = "convert {i} +level-colors black,LightGreen {o}".format(i=outCentrast_s.replace(".tif",".png"), o=outCentrast_s.replace("2.tif",".png"))
                      convertT = "convert {i} +level-colors black,DeepSkyBlue {o}".format(i=outTermrast_s.replace(".tif",".png"), o=outTermrast_s.replace("2.tif",".png"))
                      convertL = "convert {i} +level-colors black,yellow {o}".format(i=outLMidCrast_s.replace(".tif",".png"), o=outLMidCrast_s.replace("2.tif",".png"))
                      convertR = "convert {i} +level-colors black,yellow {o}".format(i=outRMidCrast_s.replace(".tif",".png"), o=outRMidCrast_s.replace("2.tif",".png"))
                      
                      convertLnKHead = "convert {i} +level-colors black,red {o}".format(i=rastVecPolysLnK_s.replace(".tif",".png"), o=rastVecPolysLnK_s.replace("2.tif",".png"))
                      # don't do stretch step for HiRISE and HiRISE anaglyph - was unnecessary and avoids problem when HiRISE contains bounding box of ctx
                      # adjust argument of level-colors to cope with all-white image
                      #convertHi = "convert {i} +level-colors black,yellow {o}".format(i=outHiRISErast_s.replace(".tif",".png"), o=outHiRISErast_s.replace("2.tif",".png"))
                      #convertHiA = "convert {i} +level-colors black,red {o}".format(i=outHiRISEArast_s.replace(".tif",".png"), o=outHiRISEArast_s.replace("2.tif",".png"))
                      convertHi = "convert {i} +level-colors ,yellow {o}".format(i=outHiRISErast_s.replace(".tif",".png"), o=outHiRISErast_s.replace("2.tif",".png"))
                      convertHiA = "convert {i} +level-colors ,red {o}".format(i=outHiRISEArast_s.replace(".tif",".png"), o=outHiRISEArast_s.replace("2.tif",".png"))
                      
                      gdaltranscmd3 = "gdal_translate -of PNG -outsize {scalex:.2}\% {scaley:.2}\% {c} {cP}".format(c=outDTM_s,cP = outDTM_s.replace(".tif",".png"), scalex=scalefactor*100, scaley=scalefactor*100)
                      # extents of all subsetted to bounding box of each context
                      gdaltranscmd4 = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outEXTALLrast_s,cP = outEXTALLrast_s.replace(".tif",".png"))
                      # don't do stretch step for HiRISE and HiRISE anaglyph - was unnecessary and avoids problem when HiRISE contains bounding box of ctx
                      #gdaltranscmdHi = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outHiRISErast_s,cP = outHiRISErast_s.replace(".tif",".png"))
                      #gdaltranscmdHiA = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outHiRISEArast_s,cP = outHiRISEArast_s.replace(".tif",".png"))
                      gdaltranscmdHi = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outHiRISErast,cP = outHiRISErast_s.replace(".tif",".png"))
                      gdaltranscmdHiA = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outHiRISEArast,cP = outHiRISEArast_s.replace(".tif",".png"))
                      
                      gdaltranscmd_vpoly = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=rastVecPolysLnK_s,cP = rastVecPolysLnK_s.replace(".tif",".png"))
                      gdaltranscmd_LyrSt = "gdal_translate -of PNG {c} -outsize {scalex:.2}\% {scaley:.2}\% {cP} -a_nodata 0".format(c=outLyrSt_s,cP = outLyrSt_s.replace(".kea",".png"), scalex=scalefactor*100, scaley=scalefactor*100)
                      
                      subprocess.call(gdaltranscmd1,shell=True)
                      subprocess.call(gdaltranscmd2,shell=True)
                      subprocess.call(gdaltranscmd2H,shell=True)
                      subprocess.call(gdaltranscmd2C,shell=True)
                      subprocess.call(gdaltranscmd2T,shell=True)
                      subprocess.call(gdaltranscmd2L,shell=True)
                      subprocess.call(gdaltranscmd2R,shell=True)
                      subprocess.call(convertH,shell=True)
                      subprocess.call(convertC,shell=True)
                      subprocess.call(convertT,shell=True)
                      subprocess.call(convertL,shell=True)
                      subprocess.call(convertR,shell=True)
                      
                      # compositing
                      composcmd1 = "composite {h} {c} {p}".format(h=outHeadrast_s.replace("2.tif",".png"), c=outCentrast_s.replace("2.tif",".png"), p=outPoints)
                      composcmd2 = "composite {p} {t} {p}".format(p=outPoints, t=outTermrast_s.replace("2.tif",".png"))
                      composcmd3 = "composite {p} {L} {p}".format(p=outPoints, L = outLMidCrast_s.replace("2.tif",".png"))
                      composcmd4 = "composite {p} {R} {p}".format(p=outPoints, R = outRMidCrast_s.replace("2.tif",".png"))
                      subprocess.call(composcmd1,shell=True)
                      subprocess.call(composcmd2,shell=True)
                      subprocess.call(composcmd3,shell=True)
                      subprocess.call(composcmd4,shell=True)
                                                                                        
                      
                                                                                                              
                      subprocess.call(gdaltranscmd3,shell=True)
                      subprocess.call(gdaltranscmd4,shell=True)
                      subprocess.call(gdaltranscmd_vpoly,shell=True)
                      if catnum in HiRISE_index:
                        subprocess.call(gdaltranscmdHi,shell=True)
                        subprocess.call(convertHi,shell=True)
                      if catnum in HiRISE_anaglyph_index:
                        subprocess.call(gdaltranscmdHiA,shell=True)
                        subprocess.call(convertHiA,shell=True)
                      
                      if not skipLyrSt:
                        subprocess.call(gdaltranscmd_LyrSt,shell=True)
                      if not(MGSmode):
                        subprocess.call(gdaltranscmd_vpoly,shell=True)
                        subprocess.call(convertLnKHead,shell=True)
                      print("Removing intermediate files.\n")
                      os.remove(outND4)
                      os.remove(outND4_s)
                      os.remove(outDTM)
                      os.remove(outDTM_a)
                      os.remove(outDTM_s)
                      os.remove(outEXTrast)
                      os.remove(outEXTrast_s)
                      os.remove(outHeadrast)
                      os.remove(outHeadrast_s)
                      os.remove(outCentrast)
                      os.remove(outCentrast_s)
                      os.remove(outTermrast)
                      os.remove(outTermrast_s)
                      os.remove(outLMidCrast)
                      os.remove(outLMidCrast_s)
                      os.remove(outRMidCrast)
                      os.remove(outRMidCrast_s)
                      os.remove(outEXTALLrast)
                      os.remove(outEXTALLrast_s)
                      if catnum in HiRISE_index:
                        os.remove(outHiRISErast)
                      #  os.remove(outHiRISErast_s)
                      if catnum in HiRISE_anaglyph_index:
                        os.remove(outHiRISEArast)
                      #  os.remove(outHiRISEArast_s)
                      if not(MGSmode):
                        os.remove(rastVecPolysLnK)
                        os.remove(rastVecPolysLnK_a)
                        os.remove(rastVecPolysLnK_s)

                      if not skipLyrSt:
                        os.remove(outLyrSt2)                              
                        os.remove(outLyrSt_s)
                      
                      

                      
                      
