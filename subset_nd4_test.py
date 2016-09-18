# create subsets of the nadir image, and rasterized shapefiles
# for the Souness GLFs that have HRSC DTM data
# crop the nadir image to the bounding box of the context shapefile of each Souness GLF
# and make rasterized images from context, extent, and head shapefiles
# for overplotting on the nd image files for example
import rsgislib
from rsgislib import imageutils, vectorutils, imagecalc
from rsgislib.imagecalc import BandDefn
import subprocess
import csv
import os
import os.path
import glob

# file paths hard-coded
sounessGLFFilePath = "/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/RemoteSensing_fromDropbox/RemoteSensing_fromDropbox_backup/"
sounessGLFFile="mmc1_HRSC+HiRISE_coverage_duplicates_possible_typos.csv"
inND4path =  '/media/davydh/TOSHIBA EXT/ioSafeBackup/RemoteSensingPlanSci_MSc/SounessCatalog3_backup/'
outND4path = 'context_subsets/'

# locations of Souness GLF individual shapefiles
contextpath = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/RemoteSensing_fromDropbox/RemoteSensing_fromDropbox_backup/SounessROIs_individual/Individual/Context/'
extentpath = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/RemoteSensing_fromDropbox/RemoteSensing_fromDropbox_backup/SounessROIs_individual/Individual/Extent/'
headpath = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/RemoteSensing_fromDropbox/RemoteSensing_fromDropbox_backup/SounessROIs_individual/Individual/heads/'

# location of all Souness extents shapefile

extent_allpath = '/home/davydh/ioSafeBackup/RemoteSensingPlanSci_MSc/PythonScripts/MarsPythonScripts/marsglaciers/SounessROIs/'
extent_allfile = 'SounessROIextents_all_Mars2000EqCyl_lat0_40.shp'
extent_all = extent_allpath + extent_allfile

centres_allfile = 'SounessROIcentres_all_Mars2000EqCyl_lat0_40.shp' 
termini_allfile = 'SounessROItermini_all_Mars2000EqCyl_lat0_40.shp'
midchL_allfile = 'SounessROIleftmidchannel_all_Mars2000EqCyl_lat0_40.shp'
midchR_allfile = 'SounessROIrightmidchannel_all_Mars2000EqCyl_lat0_40.shp'

centres_all = extent_allpath + centres_allfile 
termini_all = extent_allpath + termini_allfile
midchL_all = extent_allpath + midchL_allfile
midchR_all = extent_allpath + midchR_allfile

Gfilein = sounessGLFFilePath+sounessGLFFile
print(Gfilein)

fieldnames=['CatNum','CTXimg','Typo','offcent','Duplicate','HRSC_DTM','DTMres','HiRISE',
            'HiRISE_img','HiRISE_anaglyph','HiRISE_DTM','Hemisph','Headlon','Region','Region2',
            'Headlon180','Headlat','Termlon','Termlon180','Termlat','MidchRlon',
            'MidchRlon180','MidchRlat','MidchLlon','MidchLlon180','MidchLlat',
            'Centlon','Centlon180','Centlat','Length','Width','Area','Orientation',
            'MinElev','MaxElev','MeanElev','StdElev','Elongation','Midchlon',
            'Midchlat','distMidCCent','chanwidth','ratiooffset']


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
                if HRSC_DTMfile != 'none':
                      HRSCdir = HRSC_DTMfile[1:5]
                      nd4file = glob.glob(inND4path+HRSCdir+'/'+HRSC_DTMfile[:5]+'*nd4*.kea')
                      print(nd4file[0])                      
                      inND4 = nd4file[0]
                      outND4 = outND4path + "Souness{c:04d}_context.tif".format(c=int(catnum))
                      # stretched
                      outND4_s = outND4path + "Souness{c:04d}_context2.tif".format(c=int(catnum))

                      # image dimensions
                      statsND =  outND4path + "Souness{c:04d}_context.txt".format(c=int(catnum))

                      DTMfile = glob.glob(inND4path+HRSCdir+'/LandSerf/'+HRSC_DTMfile[:5]+'*rawAsp.kea')
                      print(DTMfile[0])
                      inDTM = DTMfile[0]
                      DTMband = inDTM.replace(".kea", "_DTM.tif")
                      outDTM = outND4path + "Souness{c:04d}DTM_context.tif".format(c=int(catnum))
                      
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
                      
                      contextvect = '{p}context_{c}.shp'.format(p=contextpath, c=int(catnum)-1)
                      extentvect = '{p}extent_{c}.shp'.format(p=extentpath, c=int(catnum)-1)
                      # these ones start at 1 rather than 0!
                      headvect =  '{p}SounessROIheads_all_Mars2000EqCyl_lat0_40_OBJ_ID__{c}.shp'.format(p = headpath, c=int(catnum))
                      try:
                        # if possible, work in rsgislib but fall back on gdalwarp if needed
                        imageutils.subset(inND4,contextvect,outND4,'GTiff',rsgislib.TYPE_8INT)
                      except:
                        gdwarpcmd = "gdalwarp -cutline {c} -crop_to_cutline {i} {out}".format(c=contextvect, i=inND4.replace("TOSHIBA EXT", "TOSHIBA\ EXT"), out=outND4)
                        print(gdwarpcmd)
                        subprocess.call(gdwarpcmd, shell=True)
                      try:
                        # if possible, work in rsgislib but fall back on gdalwarp if needed
                        if not(os.path.isfile(DTMband)):
                           imageutils.selectImageBands(inDTM, DTMband, 'GTiff', rsgislib.TYPE_32FLOAT, [2])
                        imageutils.subset(DTMband,contextvect,outDTM,'GTiff',rsgislib.TYPE_32FLOAT)
                      except:
                        gdwarpcmd = "gdalwarp -cutline {c} -crop_to_cutline {i} {out}".format(c=contextvect, i=DTMband.replace("TOSHIBA EXT", "TOSHIBA\ EXT"), out=outDTM)
                        print(gdwarpcmd)
                        subprocess.call(gdwarpcmd, shell=True)
                        
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
                        outF.write("Width,Height\n")
                        outF.write("{w},{h}".format(w=imgwidth, h=imgheight))
                      
                      print(x,y)
                      print(imgwidth,imgheight)
                      
                      DTMres = float(row['DTMres'])
                      scalefactor = DTMres / float(x)
                      print("DTM resolution is {d}, scalefactor = {s}".format(d=DTMres, s=scalefactor))
                      
                      # rasterize the shapefile
                      #gdalrastcmd = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -tr {x} {y} {vc} {vcrst}".format(x=x, y=y, vc = contextvect, vcrst = outCTXrast)
                      #gdalrastcmd = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = extentvect, vcrst = outEXTrast)
                      gdalrastcmd = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = headvect, vcrst = outHeadrast)
                      subprocess.call(gdalrastcmd, shell=True)
                      #centre
                      gdalrastcmdC = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -where 'OBJ_ID=\"{cnum}\"' -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(cnum = catnum, xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = centres_all, vcrst = outCentrast)
                      subprocess.call(gdalrastcmdC, shell=True)
                      #terminus
                      gdalrastcmdT = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -where 'OBJ_ID=\"{cnum}\"' -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(cnum = catnum, xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = termini_all, vcrst = outTermrast)
                      subprocess.call(gdalrastcmdT, shell=True)
                      #leftMid
                      gdalrastcmdL = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -where 'OBJ_ID=\"{cnum}\"' -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(cnum = catnum, xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = midchL_all, vcrst = outLMidCrast)
                      subprocess.call(gdalrastcmdL, shell=True)
                      #rightMid
                      gdalrastcmdR = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -where 'OBJ_ID=\"{cnum}\"' -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(cnum = catnum, xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = midchR_all, vcrst = outRMidCrast)
                      subprocess.call(gdalrastcmdR, shell=True)

                      gdalrastcmd2 = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = extent_all, vcrst = outEXTALLrast)
                      subprocess.call(gdalrastcmd2, shell=True)
                      
                      # stretch image to byte 8-bit by linear MinMax
                      imageutils.stretchImage(outND4,outND4_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      
                      # do the same for DTMs

                      datatype=rsgislib.TYPE_32FLOAT
                      expression = 'b1+9999'
                      bandDefns = []
                      bandDefns.append(BandDefn('b1', outDTM, 1))

                      
                      imagecalc.bandMath(outDTM_a, expression, 'GTiff', datatype, bandDefns)
                      imagecalc.imageStats(outDTM_a, statsDTM, True)
                      
                      imageutils.stretchImage(outDTM_a,outDTM_s,False,'',True,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      # do the same for shapefile rasters (though may be unnecessary)
                      #imageutils.stretchImage(outCTXrast,outCTXrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      #imageutils.stretchImage(outEXTrast,outEXTrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outHeadrast,outHeadrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outCentrast,outCentrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outTermrast,outTermrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outLMidCrast,outLMidCrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outRMidCrast,outRMidCrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outEXTALLrast,outEXTALLrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)

                      # make png files
                      gdaltranscmd1 = "gdal_translate -of PNG  {c} {cP}".format(c=outND4_s,cP = outND4_s.replace(".tif",".png"))
                      # the nodata value makes the area outside the shapefile transparent
                      #gdaltranscmd2 = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outCTXrast_s,cP = outCTXrast_s.replace(".tif",".png"))
                      #gdaltranscmd2 = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outEXTrast_s,cP = outEXTrast_s.replace(".tif",".png"))
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
                                            
                      
                      gdaltranscmd3 = "gdal_translate -of PNG -outsize {scalex:.2}\% {scaley:.2}\% {c} {cP}".format(c=outDTM_s,cP = outDTM_s.replace(".tif",".png"), scalex=scalefactor*100, scaley=scalefactor*100)
                      # extents of all subsetted to bounding box of each context
                      gdaltranscmd4 = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outEXTALLrast_s,cP = outEXTALLrast_s.replace(".tif",".png"))
                      
                      subprocess.call(gdaltranscmd1,shell=True)
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

                      
                                                                                                              
                      subprocess.call(gdaltranscmd3,shell=True)
                      subprocess.call(gdaltranscmd4,shell=True)
                      print("Removing intermediate files.\n")
                      os.remove(outND4)
                      os.remove(outND4_s)
                      os.remove(outDTM)
                      os.remove(outDTM_a)
                      os.remove(outDTM_s)
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
                      

                      
                      
