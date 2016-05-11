# create subsets of the nadir image, and rasterized shapefiles
# for the Souness GLFs that have HRSC DTM data
# crop the nadir image to the bounding box of the context shapefile of each Souness GLF
# and make rasterized images from context, extent, and head shapefiles
# for overplotting on the nd image files for example
import rsgislib
from rsgislib import imageutils, vectorutils
import subprocess
import csv
import os
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
                      # context
                      outCTXrast = outND4path + "Souness{c:04d}_contextSHP.tif".format(c=int(catnum))
                      outCTXrast_s = outND4path + "Souness{c:04d}_contextSHP2.tif".format(c=int(catnum))
                      # extent
                      outEXTrast = outND4path + "Souness{c:04d}_extentSHP.tif".format(c=int(catnum))
                      outEXTrast_s = outND4path + "Souness{c:04d}_extentSHP2.tif".format(c=int(catnum))
                      # head
                      outHeadrast = outND4path + "Souness{c:04d}_headSHP.tif".format(c=int(catnum))
                      outHeadrast_s = outND4path + "Souness{c:04d}_headSHP2.tif".format(c=int(catnum))

                      
                      
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
                                              
                      print(x,y)
                      # rasterize the shapefile
                      #gdalrastcmd = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -tr {x} {y} {vc} {vcrst}".format(x=x, y=y, vc = contextvect, vcrst = outCTXrast)
                      #gdalrastcmd = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = extentvect, vcrst = outEXTrast)
                      gdalrastcmd = "gdal_rasterize -burn 255 -of GTiff -a_nodata 0 -te {xmin} {ymin} {xmax} {ymax} -tr {x} {y} {vc} {vcrst}".format(xmin=xmin, ymin=ymin, xmax=xmax, ymax= ymax, x=x, y=y, vc = headvect, vcrst = outHeadrast)
                      subprocess.call(gdalrastcmd, shell=True)
                      # stretch image to byte 8-bit by linear MinMax
                      imageutils.stretchImage(outND4,outND4_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      # do the same for shapefile rasters (though may be unnecessary)
                      #imageutils.stretchImage(outCTXrast,outCTXrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      #imageutils.stretchImage(outEXTrast,outEXTrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)
                      imageutils.stretchImage(outHeadrast,outHeadrast_s,False,'',False,True,'GTiff',rsgislib.TYPE_8INT,imageutils.STRETCH_LINEARMINMAX)

                      # make png files
                      gdaltranscmd1 = "gdal_translate -of PNG  {c} {cP}".format(c=outND4_s,cP = outND4_s.replace(".tif",".png"))
                      # the nodata value makes the area outside the shapefile transparent
                      #gdaltranscmd2 = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outCTXrast_s,cP = outCTXrast_s.replace(".tif",".png"))
                      #gdaltranscmd2 = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outEXTrast_s,cP = outEXTrast_s.replace(".tif",".png"))
                      gdaltranscmd2 = "gdal_translate -of PNG {c} {cP} -a_nodata 0".format(c=outHeadrast_s,cP = outHeadrast_s.replace(".tif",".png"))
                      subprocess.call(gdaltranscmd1,shell=True)
                      subprocess.call(gdaltranscmd2,shell=True)
                      
