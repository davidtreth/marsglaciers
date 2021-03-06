import shapefile
import csv
import drawCircle
import math

def euclidDist(x1,y1,x2,y2):
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return dist

prj_WKT_Mars2000 = 'GEOGCS["Mars 2000",DATUM["D_Mars_2000",SPHEROID["Mars_2000_IAU_IAG",3396190.0,169.89444722361179]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
prj_WKT_Mars2000EqCyl = 'PROJCS["Mars2000_Equidistant_Cylindrical",GEOGCS["GCS_Mars_2000",DATUM["D_Mars_2000",SPHEROID["Mars_2000_IAU_IAG",3396190.0,169.8944472236118]],PRIMEM["Reference_Meridian",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Equidistant_Cylindrical"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],UNIT["Meter",1.0]]'

prj_WKT_Mars2000EqCyl_lat0_40 = 'PROJCS["Mars2000_Equidistant_Cylindrical",GEOGCS["GCS_Mars_2000",DATUM["D_Mars_2000",SPHEROID["Mars_2000_IAU_IAG",3396190.0,169.8944472236118]],PRIMEM["Reference_Meridian",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Equidistant_Cylindrical"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",40.0],UNIT["Meter",1.0]]'
proj4_Mars2000EqCyl = '+proj=eqc +lat_ts=0 +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +a=3396190 +b=3376200 +units=m +no_defs'

#csvInFile_All = open('mmc1_HRSC+HiRISE_coverage_forsummarystats_cleaned.csv','r')
csvInFile_All = open('mmc1_Souness_Alldata.csv','r')

profileOutFile = 'SounessGLFprofiles.csv'

shpPath = 'SounessROIs/'
shpOut = 'SounessROIextents_all_Mars2000EqCyl_lat0_40'
shpOut_CTX = 'SounessROIcontext_all_Mars2000EqCyl_lat0_40'
# distances * 9
shpOut_CTX9 = 'SounessROIcontext9_all_Mars2000EqCyl_lat0_40'
shpOut_H = 'SounessROIheads_all_Mars2000EqCyl_lat0_40'
shpOut_C = 'SounessROIcentres_all_Mars2000EqCyl_lat0_40'
shpOut_T = 'SounessROItermini_all_Mars2000EqCyl_lat0_40'
shpOut_MC = 'SounessROImidchannel_all_Mars2000EqCyl_lat0_40'
shpOut_LMC = 'SounessROIleftmidchannel_all_Mars2000EqCyl_lat0_40'
shpOut_RMC = 'SounessROIrightmidchannel_all_Mars2000EqCyl_lat0_40'



#mid 1 to 4 between head and midchannel centre
shpOut_mid1 = 'SounessROImidline1_all_Mars2000EqCyl_lat0_40'
shpOut_mid2 = 'SounessROImidline2_all_Mars2000EqCyl_lat0_40'
shpOut_mid3 = 'SounessROImidline3_all_Mars2000EqCyl_lat0_40'
shpOut_mid4 = 'SounessROImidline4_all_Mars2000EqCyl_lat0_40'
#mid 6 to 9 between midchannel centre and terminus
shpOut_mid6 = 'SounessROImidline6_all_Mars2000EqCyl_lat0_40'
shpOut_mid7 = 'SounessROImidline7_all_Mars2000EqCyl_lat0_40'
shpOut_mid8 = 'SounessROImidline8_all_Mars2000EqCyl_lat0_40'
shpOut_mid9 = 'SounessROImidline9_all_Mars2000EqCyl_lat0_40'


def writefootprintstoSHP(csvInFile, shpOutFile,shpOutFileCTX,shpOutFileCTX9,
                         shpOutFileH,shpOutFileC,shpOutFileT,
                         shpOutFileMCH, shpOutFileLMCH, shpOutFileRMCH,
                         shpOutFileM1,shpOutFileM2,shpOutFileM3,shpOutFileM4,shpOutFileM6,shpOutFileM7,shpOutFileM8,shpOutFileM9,
                         prjString,circradius=100.0, circN=36,skipcircles=False):

    prjfilename = shpPath + shpOutFile + ".prj"
    prjfilenameCTX =  shpPath +shpOutFileCTX + ".prj"
    prjfilenameCTX9 = shpPath + shpOutFileCTX9 + ".prj"
    prjfilenameH = shpPath + shpOutFileH + ".prj"
    prjfilenameC = shpPath + shpOutFileC + ".prj"
    prjfilenameT = shpPath + shpOutFileT + ".prj"
    prjfilenameMCH = shpPath + shpOutFileMCH + '.prj'
    prjfilenameLMCH = shpPath + shpOutFileLMCH + '.prj'
    prjfilenameRMCH = shpPath + shpOutFileRMCH + '.prj'
            

    prjfilenameM1 = shpPath + shpOutFileM1+".prj"
    prjfilenameM2 = shpPath + shpOutFileM2+".prj"
    prjfilenameM3 = shpPath + shpOutFileM3+".prj"
    prjfilenameM4 = shpPath + shpOutFileM4+".prj"
    prjfilenameM6 = shpPath + shpOutFileM6+".prj"
    prjfilenameM7 = shpPath + shpOutFileM7+".prj"
    prjfilenameM8 = shpPath + shpOutFileM8+".prj"
    prjfilenameM9 = shpPath + shpOutFileM9+".prj"
        

    w = shapefile.Writer(shapefile.POLYGON)
    w.autoBalance=0
    w.field('OBJ_ID','C','40')
    w.field('CENTRE_X','C','40')
    w.field('CENTRE_Y','C','40')
    w.field('AREA_kmsq','C','40')
    w.field('DTM_FIELD','C','40')
    w.field('DTM_RES','C','40')
    w.field('HIRISE_FN','C','40')
    w.field('HIRISE3D_FN','C','40')
    w.field('HIRISEDTM_FN','C','40')

    wctx = shapefile.Writer(shapefile.POLYGON)
    wctx.autoBalance=0
    wctx.field('OBJ_ID','C','40')
    wctx.field('CENTRE_X','C','40')
    wctx.field('CENTRE_Y','C','40')
    wctx.field('AREA_kmsq','C','40')
    wctx.field('DTM_FIELD','C','40')
    wctx.field('DTM_RES','C','40')
    wctx.field('HIRISE_FN','C','40')
    wctx.field('HIRISE3D_FN','C','40')
    wctx.field('HIRISEDTM_FN','C','40')

    wctx9 = shapefile.Writer(shapefile.POLYGON)
    wctx9.autoBalance=0
    wctx9.field('OBJ_ID','C','40')
    wctx9.field('CENTRE_X','C','40')
    wctx9.field('CENTRE_Y','C','40')
    wctx9.field('AREA_kmsq','C','40')
    wctx9.field('DTM_FIELD','C','40')
    wctx9.field('DTM_RES','C','40')
    wctx9.field('HIRISE_FN','C','40')
    wctx9.field('HIRISE3D_FN','C','40')
    wctx9.field('HIRISEDTM_FN','C','40')


    if skipcircles == False:
        w_h = shapefile.Writer(shapefile.POLYGON)
        w_h.autoBalance=0
        w_h.field('OBJ_ID','C','40')
        w_h.field('HEAD_X','C','40')
        w_h.field('HEAD_Y','C','40')
        w_h.field('AREA_kmsq','C','40')
        w_h.field('DTM_FIELD','C','40')
        w_h.field('DTM_RES','C','40')
        w_h.field('HIRISE_FN','C','40')
        w_h.field('HIRISE3D_FN','C','40')
        w_h.field('HIRISEDTM_FN','C','40')

        w_c = shapefile.Writer(shapefile.POLYGON)
        w_c.autoBalance=0
        w_c.field('OBJ_ID','C','40')
        w_c.field('CENTRE_X','C','40')
        w_c.field('CENTRE_Y','C','40')
        w_c.field('AREA_kmsq','C','40')
        w_c.field('DTM_FIELD','C','40')
        w_c.field('DTM_RES','C','40')
        w_c.field('HIRISE_FN','C','40')
        w_c.field('HIRISE3D_FN','C','40')
        w_c.field('HIRISEDTM_FN','C','40')


        w_t = shapefile.Writer(shapefile.POLYGON)
        w_t.autoBalance=0
        w_t.field('OBJ_ID','C','40')
        w_t.field('TERMINUS_X','C','40')
        w_t.field('TERMINUS_Y','C','40')
        w_t.field('AREA_kmsq','C','40')
        w_t.field('DTM_FIELD','C','40')
        w_t.field('DTM_RES','C','40')
        w_t.field('HIRISE_FN','C','40')
        w_t.field('HIRISE3D_FN','C','40')
        w_t.field('HIRISEDTM_FN','C','40')

        w_m1 = shapefile.Writer(shapefile.POLYGON)
        w_m1.autoBalance=0
        w_m1.field('OBJ_ID','C','40')
        w_m1.field('MID1_X','C','40')
        w_m1.field('MID1_Y','C','40')
        w_m1.field('AREA_kmsq','C','40')
        w_m1.field('DTM_FIELD','C','40')
        w_m1.field('DTM_RES','C','40')
        w_m1.field('HIRISE_FN','C','40')
        w_m1.field('HIRISE3D_FN','C','40')
        w_m1.field('HIRISEDTM_FN','C','40')

        
        w_m2 = shapefile.Writer(shapefile.POLYGON)
        w_m2.autoBalance=0
        w_m2.field('OBJ_ID','C','40')
        w_m2.field('MID2_X','C','40')
        w_m2.field('MID2_Y','C','40')
        w_m2.field('AREA_kmsq','C','40')
        w_m2.field('DTM_FIELD','C','40')
        w_m2.field('DTM_RES','C','40')
        w_m2.field('HIRISE_FN','C','40')
        w_m2.field('HIRISE3D_FN','C','40')
        w_m2.field('HIRISEDTM_FN','C','40')

        w_m3 = shapefile.Writer(shapefile.POLYGON)
        w_m3.autoBalance=0
        w_m3.field('OBJ_ID','C','40')
        w_m3.field('MID3_X','C','40')
        w_m3.field('MID3_Y','C','40')
        w_m3.field('AREA_kmsq','C','40')
        w_m3.field('DTM_FIELD','C','40')
        w_m3.field('DTM_RES','C','40')
        w_m3.field('HIRISE_FN','C','40')
        w_m3.field('HIRISE3D_FN','C','40')
        w_m3.field('HIRISEDTM_FN','C','40')

        w_m4 = shapefile.Writer(shapefile.POLYGON)
        w_m4.autoBalance=0
        w_m4.field('OBJ_ID','C','40')
        w_m4.field('MID4_X','C','40')
        w_m4.field('MID4_Y','C','40')
        w_m4.field('AREA_kmsq','C','40')
        w_m4.field('DTM_FIELD','C','40')
        w_m4.field('DTM_RES','C','40')
        w_m4.field('HIRISE_FN','C','40')
        w_m4.field('HIRISE3D_FN','C','40')
        w_m4.field('HIRISEDTM_FN','C','40')

        w_midch = shapefile.Writer(shapefile.POLYGON)
        w_midch.autoBalance=0
        w_midch.field('OBJ_ID','C','40')
        w_midch.field('MIDCH_X','C','40')
        w_midch.field('MIDCH_Y','C','40')
        w_midch.field('AREA_kmsq','C','40')
        w_midch.field('DTM_FIELD','C','40')
        w_midch.field('DTM_RES','C','40')
        w_midch.field('HIRISE_FN','C','40')
        w_midch.field('HIRISE3D_FN','C','40')
        w_midch.field('HIRISEDTM_FN','C','40')
        
        w_midchL = shapefile.Writer(shapefile.POLYGON)
        w_midchL.autoBalance=0
        w_midchL.field('OBJ_ID','C','40')
        w_midchL.field('MIDCH_X','C','40')
        w_midchL.field('MIDCH_Y','C','40')
        w_midchL.field('AREA_kmsq','C','40')
        w_midchL.field('DTM_FIELD','C','40')
        w_midchL.field('DTM_RES','C','40')
        w_midchL.field('HIRISE_FN','C','40')
        w_midchL.field('HIRISE3D_FN','C','40')
        w_midchL.field('HIRISEDTM_FN','C','40')
        
        w_midchR = shapefile.Writer(shapefile.POLYGON)
        w_midchR.autoBalance=0
        w_midchR.field('OBJ_ID','C','40')
        w_midchR.field('MIDCH_X','C','40')
        w_midchR.field('MIDCH_Y','C','40')
        w_midchR.field('AREA_kmsq','C','40')
        w_midchR.field('DTM_FIELD','C','40')
        w_midchR.field('DTM_RES','C','40')
        w_midchR.field('HIRISE_FN','C','40')
        w_midchR.field('HIRISE3D_FN','C','40')
        w_midchR.field('HIRISEDTM_FN','C','40')

        w_m6 = shapefile.Writer(shapefile.POLYGON)
        w_m6.autoBalance=0
        w_m6.field('OBJ_ID','C','40')
        w_m6.field('MID6_X','C','40')
        w_m6.field('MID6_Y','C','40')
        w_m6.field('AREA_kmsq','C','40')
        w_m6.field('DTM_FIELD','C','40')
        w_m6.field('DTM_RES','C','40')
        w_m6.field('HIRISE_FN','C','40')
        w_m6.field('HIRISE3D_FN','C','40')
        w_m6.field('HIRISEDTM_FN','C','40')

        w_m7 = shapefile.Writer(shapefile.POLYGON)
        w_m7.autoBalance=0
        w_m7.field('OBJ_ID','C','40')
        w_m7.field('MID7_X','C','40')
        w_m7.field('MID7_Y','C','40')
        w_m7.field('AREA_kmsq','C','40')
        w_m7.field('DTM_FIELD','C','40')
        w_m7.field('DTM_RES','C','40')
        w_m7.field('HIRISE_FN','C','40')
        w_m7.field('HIRISE3D_FN','C','40')
        w_m7.field('HIRISEDTM_FN','C','40')

        w_m8 = shapefile.Writer(shapefile.POLYGON)
        w_m8.autoBalance=0
        w_m8.field('OBJ_ID','C','40')
        w_m8.field('MID8_X','C','40')
        w_m8.field('MID8_Y','C','40')
        w_m8.field('AREA_kmsq','C','40')
        w_m8.field('DTM_FIELD','C','40')
        w_m8.field('DTM_RES','C','40')
        w_m8.field('HIRISE_FN','C','40')
        w_m8.field('HIRISE3D_FN','C','40')
        w_m8.field('HIRISEDTM_FN','C','40')

        w_m9 = shapefile.Writer(shapefile.POLYGON)
        w_m9.autoBalance=0
        w_m9.field('OBJ_ID','C','40')
        w_m9.field('MID9_X','C','40')
        w_m9.field('MID9_Y','C','40')
        w_m9.field('AREA_kmsq','C','40')
        w_m9.field('DTM_FIELD','C','40')
        w_m9.field('DTM_RES','C','40')
        w_m9.field('HIRISE_FN','C','40')
        w_m9.field('HIRISE3D_FN','C','40')
        w_m9.field('HIRISEDTM_FN','C','40')

    
    csv_reader = csv.reader(csvInFile)
    for row in enumerate(csv_reader):
        if row[0]==0:
            continue
        else:
            Hx = float(row[1][0])
            Hy = float(row[1][1])
            Cx = float(row[1][2])
            Cy = float(row[1][3])
            Tx = float(row[1][4])
            Ty = float(row[1][5])
            LCx = float(row[1][6])
            LCy = float(row[1][7])
            RCx = float(row[1][8])
            RCy = float(row[1][9])

            MidCHx = (LCx + RCx) / 2.0
            MidCHy = (LCy + RCy) / 2.0
            MidCHr = euclidDist(Hx,Hy,MidCHx,MidCHy)    

            Mid1x = Hx + 0.2*(MidCHx - Hx)
            Mid1y = Hy + 0.2*(MidCHy - Hy)
            Mid1r = euclidDist(Hx,Hy,Mid1x,Mid1y)
            
            Mid2x = Hx + 0.4*(MidCHx - Hx)
            Mid2y = Hy + 0.4*(MidCHy - Hy)
            Mid2r = euclidDist(Hx,Hy,Mid2x,Mid2y)
                        
            Mid3x = Hx + 0.6*(MidCHx - Hx)
            Mid3y = Hy + 0.6*(MidCHy - Hy)
            Mid3r = euclidDist(Hx,Hy,Mid3x,Mid3y)
            
            Mid4x = Hx + 0.8*(MidCHx - Hx)
            Mid4y = Hy + 0.8*(MidCHy - Hy)
            Mid4r = euclidDist(Hx,Hy,Mid4x,Mid4y)
            
            Mid6x = MidCHx + 0.2*(Tx - MidCHx)
            Mid6y = MidCHy + 0.2*(Ty - MidCHy)
            Mid6r = MidCHr + euclidDist(MidCHx,MidCHy,Mid6x,Mid6y)
            
            Mid7x = MidCHx + 0.4*(Tx - MidCHx)
            Mid7y = MidCHy + 0.4*(Ty - MidCHy)
            Mid7r = MidCHr + euclidDist(MidCHx,MidCHy,Mid7x,Mid7y)
            
                        
            Mid8x = MidCHx + 0.6*(Tx - MidCHx)
            Mid8y = MidCHy + 0.6*(Ty - MidCHy)
            Mid8r = MidCHr + euclidDist(MidCHx,MidCHy,Mid8x,Mid8y)                

                        
            Mid9x = MidCHx + 0.8*(Tx - MidCHx)
            Mid9y = MidCHy + 0.8*(Ty - MidCHy)
            Mid9r = MidCHr + euclidDist(MidCHx,MidCHy,Mid9x,Mid9y)                


            Tr = MidCHr + euclidDist(MidCHx,MidCHy,Tx,Ty)
            
            catnum = int(row[1][14])


            widthvecRx = RCx - Cx
            widthvecRy = RCy - Cy
            widthvecLx = LCx - Cx
            widthvecLy = LCy - Cy
            HRx = Hx + widthvecRx
            HRy = Hy + widthvecRy
            HLx = Hx + widthvecLx
            HLy = Hy + widthvecLy
            TRx = Tx + widthvecRx
            TRy = Ty + widthvecRy
            TLx = Tx + widthvecLx
            TLy = Ty + widthvecLy        

            Hctxx = Hx + 2*(Hx-Cx)
            Hctxy = Hy + 2*(Hy-Cy)
            Tctxx = Tx + 2*(Tx-Cx)
            Tctxy = Ty + 2*(Ty-Cy)
            HRctxx = Hctxx + 3*widthvecRx
            HRctxy = Hctxy + 3*widthvecRy
            HLctxx = Hctxx + 3*widthvecLx
            HLctxy = Hctxy + 3*widthvecLy
            TRctxx = Tctxx + 3*widthvecRx
            TRctxy = Tctxy + 3*widthvecRy
            TLctxx = Tctxx + 3*widthvecLx
            TLctxy = Tctxy + 3*widthvecLy
            RCctxx = Cx + 3*widthvecRx
            RCctxy = Cy + 3*widthvecRy
            LCctxx = Cx + 3*widthvecLx
            LCctxy = Cy + 3*widthvecLy

            Hctx9x = Hx + 8*(Hx-Cx)
            Hctx9y = Hy + 8*(Hy-Cy)
            Tctx9x = Tx + 8*(Tx-Cx)
            Tctx9y = Ty + 8*(Ty-Cy)
            HRctx9x = Hctx9x + 9*widthvecRx
            HRctx9y = Hctx9y + 9*widthvecRy
            HLctx9x = Hctx9x + 9*widthvecLx
            HLctx9y = Hctx9y + 9*widthvecLy
            TRctx9x = Tctx9x + 9*widthvecRx
            TRctx9y = Tctx9y + 9*widthvecRy
            TLctx9x = Tctx9x + 9*widthvecLx
            TLctx9y = Tctx9y + 9*widthvecLy
            RCctx9x = Cx + 9*widthvecRx
            RCctx9y = Cy + 9*widthvecRy
            LCctx9x = Cx + 9*widthvecLx
            LCctx9y = Cy + 9*widthvecLy
            
            DTMfn = '"'+row[1][17]+'"'
            DTMres = row[1][18] #could be a number except for some fields that are not numbers
            HiRISEfn = '"'+row[1][19]+'"'
            HiRISE3Dfn = '"'+row[1][20]+'"'
            HiRISEDTMfn = '"'+row[1][21]+'"'
            area = float(row[1][12])

            profile = [catnum,DTMfn,Hx,Hy,0.0,Mid1x,Mid1y,Mid1r,Mid2x,Mid2y,Mid2r,Mid3x,Mid3y,Mid3r,Mid4x,Mid4y,Mid4r,MidCHx,MidCHy,MidCHr,Mid6x,Mid6y,Mid6r,Mid7x,Mid7y,Mid7r,Mid8x,Mid8y,Mid8r,Mid9x,Mid9y,Mid9r,Tx,Ty,Tr]
            profiles.append(profile)

                
                       

#w.poly(parts=[[[0,0],[2,3],[2,6],[-2,3],[0,0]]])
            polygon_points = [[[HRx,HRy],[RCx,RCy],[TRx,TRy],[Tx,Ty],[TLx,TLy],[LCx,LCy],[HLx,HLy],[Hx,Hy],[HRx,HRy]]]
            polygon_points_ctx = [[[HRctxx,HRctxy],[RCctxx,RCctxy],[TRctxx,TRctxy],[Tctxx,Tctxy],[TLctxx,TLctxy],[LCctxx,LCctxy],[HLctxx,HLctxy],[Hctxx,Hctxy],[HRctxx,HRctxy]]]
            polygon_points_ctx9 = [[[HRctx9x,HRctx9y],[RCctx9x,RCctx9y],[TRctx9x,TRctx9y],[Tctx9x,Tctx9y],[TLctx9x,TLctx9y],[LCctx9x,LCctx9y],[HLctx9x,HLctx9y],[Hctx9x,Hctx9y],[HRctx9x,HRctx9y]]]
            if skipcircles==False:
                heads_circ_points = drawCircle.generateCirclePointsZip(Hx,Hy,circradius,circN)
                centres_circ_points = drawCircle.generateCirclePointsZip(Cx,Cy,circradius,circN)
                termini_circ_points = drawCircle.generateCirclePointsZip(Tx,Ty,circradius,circN)

                mid1_circ_points = drawCircle.generateCirclePointsZip(Mid1x,Mid1y,circradius,circN)
                mid2_circ_points = drawCircle.generateCirclePointsZip(Mid2x,Mid2y,circradius,circN)
                mid3_circ_points = drawCircle.generateCirclePointsZip(Mid3x,Mid3y,circradius,circN)
                mid4_circ_points = drawCircle.generateCirclePointsZip(Mid4x,Mid4y,circradius,circN)
                midch_circ_points = drawCircle.generateCirclePointsZip(MidCHx,MidCHy,circradius,circN)
                midchL_circ_points = drawCircle.generateCirclePointsZip(LCx,LCy,circradius,circN)
                midchR_circ_points = drawCircle.generateCirclePointsZip(RCx,RCy,circradius,circN)
                mid6_circ_points = drawCircle.generateCirclePointsZip(Mid6x,Mid6y,circradius,circN)
                mid7_circ_points = drawCircle.generateCirclePointsZip(Mid7x,Mid7y,circradius,circN)
                mid8_circ_points = drawCircle.generateCirclePointsZip(Mid8x,Mid8y,circradius,circN)
                mid9_circ_points = drawCircle.generateCirclePointsZip(Mid9x,Mid9y,circradius,circN)

                w_h.poly(parts=heads_circ_points)
                w_c.poly(parts=centres_circ_points)
                w_t.poly(parts=termini_circ_points)

                w_m1.poly(parts=mid1_circ_points)
                w_m2.poly(parts=mid2_circ_points)
                w_m3.poly(parts=mid3_circ_points)
                w_m4.poly(parts=mid4_circ_points)
                w_midch.poly(parts=midch_circ_points)
                w_midchL.poly(parts=midchL_circ_points)
                w_midchR.poly(parts=midchR_circ_points)
                                                
                w_m6.poly(parts=mid6_circ_points)
                w_m7.poly(parts=mid7_circ_points)
                w_m8.poly(parts=mid8_circ_points)
                w_m9.poly(parts=mid9_circ_points)
                

                w_h.record(catnum,Hx,Hy,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_c.record(catnum,Cx,Cy,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_t.record(catnum,Tx,Ty,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)

                w_m1.record(catnum,Mid1x,Mid1y,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_m2.record(catnum,Mid2x,Mid2y,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_m3.record(catnum,Mid3x,Mid3y,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_m4.record(catnum,Mid4x,Mid4y,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_midch.record(catnum,MidCHx,MidCHy,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_midchL.record(catnum,LCx,LCy,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_midchR.record(catnum,RCx,RCy,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_m6.record(catnum,Mid6x,Mid6y,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_m7.record(catnum,Mid7x,Mid7y,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_m8.record(catnum,Mid8x,Mid8y,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                w_m9.record(catnum,Mid9x,Mid9y,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
                
                

            w.poly(parts=polygon_points)
            wctx.poly(parts=polygon_points_ctx)
            wctx9.poly(parts=polygon_points_ctx9)

            print polygon_points
            w.record(catnum,Cx,Cy,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
            wctx.record(catnum,Cx,Cy,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
            wctx9.record(catnum,Cx,Cy,area,DTMfn,DTMres,HiRISEfn,HiRISE3Dfn,HiRISEDTMfn)
    print "number of shapes: ",len(w.shapes())
    w.save(shpPath+shpOutFile)
    prj=open(prjfilename,"w")
    prj.write(prjString)
    prj.close()

    wctx.save(shpPath+shpOutFileCTX)
    prj=open(prjfilenameCTX,"w")
    prj.write(prjString)
    prj.close()

    wctx9.save(shpPath+shpOutFileCTX9)
    prj=open(prjfilenameCTX9,"w")
    prj.write(prjString)
    prj.close()

    if skipcircles==False:
        w_h.save(shpPath+shpOutFileH)
        prj=open(prjfilenameH,"w")
        prj.write(prjString)
        prj.close()

        w_c.save(shpPath+shpOutFileC)
        prj=open(prjfilenameC,"w")
        prj.write(prjString)
        prj.close()

        w_t.save(shpPath+shpOutFileT)
        prj=open(prjfilenameT,"w")
        prj.write(prjString)
        prj.close()

        w_m1.save(shpPath+shpOutFileM1)
        prj=open(prjfilenameM1,"w")
        prj.write(prjString)
        prj.close()
        
        w_m2.save(shpPath+shpOutFileM2)
        prj=open(prjfilenameM2,"w")
        prj.write(prjString)
        prj.close()
        
        w_m3.save(shpPath+shpOutFileM3)
        prj=open(prjfilenameM3,"w")
        prj.write(prjString)
        prj.close()
        
        w_m4.save(shpPath+shpOutFileM4)
        prj=open(prjfilenameM4,"w")
        prj.write(prjString)
        prj.close()
        
        w_midch.save(shpPath+shpOutFileMCH)
        prj=open(prjfilenameMCH,"w")
        prj.write(prjString)
        prj.close()
        
        w_midchL.save(shpPath+shpOutFileLMCH)
        prj=open(prjfilenameLMCH,"w")
        prj.write(prjString)
        prj.close()
        
        w_midchR.save(shpPath+shpOutFileRMCH)
        prj=open(prjfilenameRMCH,"w")
        prj.write(prjString)
        prj.close()
        
        w_m6.save(shpPath+shpOutFileM6)
        prj=open(prjfilenameM6,"w")
        prj.write(prjString)
        prj.close()
        
        w_m7.save(shpPath+shpOutFileM7)
        prj=open(prjfilenameM7,"w")
        prj.write(prjString)
        prj.close()
        
        w_m8.save(shpPath+shpOutFileM8)
        prj=open(prjfilenameM8,"w")
        prj.write(prjString)
        prj.close()
        w_m9.save(shpPath+shpOutFileM9)
        prj=open(prjfilenameM9,"w")
        prj.write(prjString)
        prj.close()
    
    try:
        from StringIO import StringIO
    except ImportError:
        from io import BytesIO as StringIO
    shp = StringIO()
    shx = StringIO()
    dbf = StringIO()
    w.saveShp(shp)
    w.saveShx(shx)
    w.saveDbf(dbf)
    wctx.saveShp(shp)
    wctx.saveShx(shx)
    wctx.saveDbf(dbf)
    wctx9.saveShp(shp)
    wctx9.saveShx(shx)
    wctx9.saveDbf(dbf)
    if skipcircles==False:
        w_h.saveShp(shp)
        w_h.saveShx(shx)
        w_h.saveDbf(dbf)
        w_c.saveShp(shp)
        w_c.saveShx(shx)
        w_c.saveDbf(dbf)
        w_t.saveShp(shp)
        w_t.saveShx(shx)
        w_t.saveDbf(dbf)

    shp = shx = dbf = None
profiles = []
writefootprintstoSHP(csvInFile_All, shpOut,shpOut_CTX,shpOut_CTX9,
                     shpOut_H,shpOut_C,shpOut_T,
                     shpOut_MC, shpOut_LMC, shpOut_RMC,
                     shpOut_mid1,shpOut_mid2,shpOut_mid3,shpOut_mid4,shpOut_mid6,shpOut_mid7,shpOut_mid8,shpOut_mid9,
                     prj_WKT_Mars2000EqCyl_lat0_40)

# write out profiles
with open(profileOutFile,'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter = ',')
    for p in profiles:
        spamwriter.writerow(p)





#shpOut_MC = 'SounessROImidchannel_all_Mars2000EqCyl_lat0_40'

#mid 1 to 4 between head and midchannel centre
#shpOut_mid1 = 'SounessROImidline1_all_Mars2000EqCyl_lat0_40'
#shpOut_mid2 = 'SounessROImidline2_all_Mars2000EqCyl_lat0_40'
#shpOut_mid3 = 'SounessROImidline3_all_Mars2000EqCyl_lat0_40'
#shpOut_mid4 = 'SounessROImidline4_all_Mars2000EqCyl_lat0_40'
#mid 6 to 9 between midchannel centre and terminus
#shpOut_mid6 = 'SounessROImidline6_all_Mars2000EqCyl_lat0_40'
#shpOut_mid7 = 'SounessROImidline7_all_Mars2000EqCyl_lat0_40'
#shpOut_mid8 = 'SounessROImidline8_all_Mars2000EqCyl_lat0_40'
#shpOut_mid9 = 'SounessROImidline9_all_Mars2000EqCyl_lat0_40'

csvInFile_All.close()



# vector from C --> LC, C --> RC
# thus find H-->LH, H-->RH, T-->LT, T-->RT
# rectangle polygon points LH, RH, LT, RT


