#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 14:33:21 2021

@author: komal
"""


from nipype.interfaces.fsl import BET
import matplotlib.pylab as plt
from skimage.io import imread
from skimage.color import rgb2gray
from skimage import filters
import matplotlib.pyplot as plt 
import os
import numpy as np
from nibabel.testing import data_path
import cv2
import nibabel as nib
import cv2
import glob
from scipy.stats import norm, kurtosis
import os
import shutil
import sys
import math
import os
import nipype.interfaces.spm as spm
os.environ['SPM_PATH']='/media/ninslab/DATA1/spm12'
spm.SPMCommand.set_mlab_paths(paths=os.environ['SPM_PATH'])
direc="folder_name/QC_folder/MRI/*"
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    sub = sorted(glob.glob(folder[z]+"/*"))
    for x in range(len(sub)):
        dirpath = (folder[z]+"/")
        os.chdir(dirpath)
        if ".nii" in sub[x]:
            os.rename(sub[x], 'HU_0.nii')
                #os.system('med2image -i HU_0.nii -d jpeg')
                
                
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    l=0
    for nv in range(6):
        sub = sorted(glob.glob(folder[z]+"/*")) 
        for x in range(len(sub)):
            dirpath = (folder[z]+"/")
            os.chdir(dirpath)
            if "HU_"+str(l) in sub[x]:
                mask=BET(in_file=sub[x])
                res=mask.run(surfaces=True)
                img_orig = nib.load(folder[z]+'/HU_0.nii')
                data_orig = img_orig.get_fdata()
                sub = (glob.glob(folder[z]+"/*"))
                for x in range(len(sub)):
                    if "HU_" + str(l) + "_brain_outskin_mask" in sub[x]:          
                        mask=sub[x]
                        img_mask=nib.load(mask)
                        data_mask=img_mask.get_fdata() 
                        roi=np.empty(data_orig.shape)
                        l=l+1
                        for i in range(len(data_orig[:,1,1])):          
                            for j in range(len(data_orig[1,:,1])):
                                for k in range(len(data_orig[1,1,:])):
                                    if data_mask[i,j,k] == 1:
                                        roi[i,j,k] =data_orig[i,j,k]
                        ni_img=nib.Nifti1Image(roi,img_orig.affine)
                        nib.save(ni_img, dirpath+'HU_' + str(l)+'.nii')                    

                                                                                  
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    l=0
    sub = sorted(glob.glob(folder[z]+"/*")) 
    for x in range(len(sub)):
        dirpath = (folder[z]+"/")
        os.chdir(dirpath)
        if "HU_0.nii" in sub[x]:
            seg = spm.NewSegment()
            seg.inputs.channel_files = sub[x]
            seg.inputs.channel_info=(0.001, 60, (True, True))
            tissue1 = (('/media/ninslab/DATA1/spm12/tpm/TPM.nii', 1), 1, (True,False), (False, False))
            tissue2 = (('/media/ninslab/DATA1/spm12/tpm/TPM.nii', 2), 1, (True,False), (False, False))
            tissue3 = (('/media/ninslab/DATA1/spm12/tpm/TPM.nii', 3), 2, (True,False), (False, False))
            tissue4 = (('/media/ninslab/DATA1/spm12/tpm/TPM.nii', 4), 3, (True,False), (False, False))
            tissue5 = (('/media/ninslab/DATA1/spm12/tpm/TPM.nii', 5), 4, (True,False), (False, False))
            tissue6 = (('/media/ninslab/DATA1/spm12/tpm/TPM.nii', 6), 2, (False,False), (False, False))
            seg.inputs.tissues = [tissue1, tissue2, tissue3, tissue4, tissue5, tissue6]
            seg.inputs.sampling_distance=3
            seg.inputs.warping_regularization=[0, 0.001, 0.5, 0.05, 0.2]
            seg.run()
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    sub = sorted(glob.glob(folder[z]+"/*"))
    for x in range(len(sub)):
        if "c1HU_0" in sub[x]:
            dirpath = (folder[z]+"/")
            os.chdir(dirpath)
            os.rename(sub[x], 'grey_0.nii')
        if "c2HU_0" in sub[x]:
            dirpath = (folder[z]+"/")
            os.chdir(dirpath)
            os.rename(sub[x], 'white_0.nii')
        if "c3HU_0" in sub[x]:
            dirpath = (folder[z]+"/")
            os.chdir(dirpath)
            os.rename(sub[x], 'csf_0.nii')
        if "c4HU_0" in sub[x]:
            dirpath = (folder[z]+"/")
            os.chdir(dirpath)
            os.rename(sub[x], 'extra1.nii')
        if "c5HU_0" in sub[x]:
            dirpath = (folder[z]+"/")
            os.chdir(dirpath)
            os.rename(sub[x], 'extra2.nii')
folder = sorted(glob.glob(direc))
snr, msi_var, name, cnr, cvnr, tctv, cjv, kurt, svnr, msi_mn=[], [],[], [], [], [], [], [], [], []
for z in range(len(folder)):
    name.append(os.path.basename(folder[z]))
    sub = sorted(glob.glob(folder[z]+"/*"))
    for x in range(len(sub)):
        if "HU_0.nii" in sub[x]:         
            original=sub[x]
            img_original = nib.load(original)
            data_original = img_original.get_fdata()
        if "grey_0.nii" in sub[x]:
            grey=sub[x]
            grey_img=nib.load(grey)
            grey_data=grey_img.get_fdata()
            roi_g=np.empty(grey_data.shape)
            for i in range(len(data_original[:,1,1])):          
                for j in range(len(data_original[1,:,1])):
                    for k in range(len(data_original[1,1,:])):
                        if grey_data[i,j,k]>0:
                            roi_g[i,j,k] =data_original[i,j,k]
                # xg,yg,zg = np.where(roi_g!=0) 
                # roi_g1=roi_g[min(xg):max(xg)+1,min(yg):max(yg)+1,min(zg):max(zg)+1]
                                
        if "white_0.nii" in sub[x]:
            white=sub[x]
            white_img=nib.load(white)
            white_data=white_img.get_fdata()
            roi_w=np.empty(white_data.shape)
            for i in range(len(data_original[:,1,1])):          
                for j in range(len(data_original[1,:,1])):
                    for k in range(len(data_original[1,1,:])):
                        if white_data[i,j,k]>0:
                            roi_w[i,j,k] =data_original[i,j,k]
                # xw,yw,zw = np.where(roi_w!=0) 
                # roi_w1=roi_w[min(xw):max(xw)+1,min(yw):max(yw)+1,min(zw):max(zw)+1]
        if "HU_5_brain_outskin_mask.nii" in sub[x]:  
            mask_f=sub[x]
            img_mask_f = nib.load(mask_f)
            data_mask_f = img_mask_f.get_fdata()
            roi=np.zeros(data_original.shape)
            background=np.empty(data_original.shape)
            for i in range(len(data_original[:,1,1])):          
                for j in range(len(data_original[1,:,1])):
                    for k in range(len(data_original[1,1,:])):
                        if data_mask_f[i,j,k]!= 1:
                            background[i,j,k] =data_original[i,j,k]
                                
                        else:
                            roi[i,j,k] =data_original[i,j,k]
            msi=np.empty(data_original[1,1,:].shape)*[0]
            for k in range(len(data_original[1,1,:])):
                msi[k]=np.mean(data_original[:,:,k])
            xr,yr,zr = np.where(roi!=0) 
            roi_r1=roi[min(xr):max(xr)+1,min(yr):max(yr)+1,min(zr):max(zr)+1]
            xb,yb,zb = np.where(background!=0) 
            roi_b1=background[min(xb):max(xb)+1,min(yb):max(yb)+1,min(zb):max(zb)+1]
    fileno = os.path.basename(folder[z])
    os.chdir("/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/MRI/"+fileno+"/")
    snr.append((20*math.log10(np.mean(roi)/np.std(background))))
    msi_var.append((np.var(msi)))
    cnr.append(((abs((np.mean(roi_g)-np.mean(roi_w)))/(np.std(background)))))
    cvnr.append(((abs(np.std(roi_g)-np.std(roi_w)))/(np.std(background))))
    tctv.append(((abs(np.mean(roi_g)-np.mean(roi_w)))/(np.sqrt(np.square(np.std(roi_g))+np.square(np.std(roi_w))))))
    cjv.append(((np.std(roi_w)-np.std(roi_g))/(np.mean(roi_w))))
    kurt.append((np.mean(kurtosis(data_original))))
    svnr.append((20*math.log10(np.var(roi)/np.var(background))))
import xlsxwriter
workbook = xlsxwriter.Workbook('qualityreport.xlsx', {'nan_inf_to_errors':True})
worksheet = workbook.add_worksheet()
iqm = {'Subject_ID': name,'MSI_VAR':msi_var, 'SNR': snr, 'CNR':cnr,'KURTOSIS':kurt, 'CVNR':cvnr, 'TCTV':tctv, 'CJV':cjv, 'SVNR':svnr}
col_num = 0
for key, value in iqm.items():
    worksheet.write(0, col_num, key)
    worksheet.write_column(1,col_num, value)
    col_num +=1
workbook.close()


import pandas as pd
read_file = pd.read_excel ("qualityreport.xlsx")
read_file.to_csv ("qualityreport.csv", 
                  index = None,
                  header=True)

from nipype.interfaces.fsl import BET
import matplotlib.pylab as plt
from skimage.io import imread
from skimage.color import rgb2gray
from skimage import filters
import matplotlib.pyplot as plt 
import os
import numpy as np
from nibabel.testing import data_path
import nibabel as nib
import glob
from scipy.stats import norm, kurtosis
import os
import shutil
import sys
import math
import os
import nipype.interfaces.spm as spm
import pathlib
import datetime

Voxel_Size, Scan_Date, Scan_Time, Dimensions, Offset, Matrix_Size, Slices,name = [],[],[],[],[],[],[],[]
direc="/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/MRI/*"
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    name.append(os.path.basename(folder[z]))
    l=0
    sub = sorted(glob.glob(folder[z]+"/*")) 
    for x in range(len(sub)):
        if "HU_0.nii" in sub[x]:      
            Num = list()
            slices1=list()
            img = nib.load(sub[x])
            hdr = img.header
            voxel_size1= hdr.get_zooms()
            voxel_size  ='X'.join([str(i) for i in voxel_size1])
            D = hdr.get_data_dtype()
            Datatype = D.name
            dimensions1 = hdr.get_data_shape()
            dimensions = 'X'.join([str(i) for i in dimensions1])
            offset = hdr.get_data_offset()
            Num.append(dimensions1[0])
            Num.append(dimensions1[1])
            num = 'X'.join([str(i) for i in Num])
            slices1.append(dimensions1[2])
            slices ='X'.join([str(i) for i in slices1])
            fname = pathlib.Path(sub[x])
            Scan_date1 = datetime.datetime.fromtimestamp(fname.stat().st_mtime).date()
            Scan_date = Scan_date1.strftime('%m/%d/%Y')
            St = datetime.datetime.fromtimestamp(fname.stat().st_mtime).time()
            scan_time = St.isoformat()
        fileno = os.path.basename(folder[z])
        os.chdir("/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/MRI/"+fileno+"/")
        Voxel_Size.append(voxel_size)
        Scan_Date.append(Scan_date)
        Scan_Time.append(scan_time)
        Dimensions.append(dimensions)
        Offset.append(offset)
        Matrix_Size.append(num)
        Slices.append(slices)
import xlsxwriter
workbook = xlsxwriter.Workbook('acquisition_param.xlsx', {'nan_inf_to_errors':True})
worksheet = workbook.add_worksheet()
iqm = {'Subject_ID': name,'Voxel Size': Voxel_Size, 'Scan Date': Scan_Date, 'Scan Time': Scan_Time, 'Dimensions': Dimensions, 'Offset': Offset, 'Matrix':Matrix_Size, 'Slices': Slices }
col_num = 0
for key, value in iqm.items():
    worksheet.write(0, col_num, key)
    worksheet.write_column(1,col_num, value)
    col_num +=1
workbook.close()
import pandas as pd
read_file = pd.read_excel ("acquisition_param.xlsx")
read_file.to_csv ("acquisition_param.csv", 
                  index = None,
                  header=True)


from os import path
direc1="/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/MRI/*"
folder = sorted(glob.glob(direc1))
for z in range(len(folder)):
    sub = sorted(glob.glob(folder[z]+"/*"))
    path_new_jpeg = folder[z] + "/jpeg"
    os.mkdir(path_new_jpeg)
    for x in range(len(sub)):
        if "BiasField_HU_0.nii" in sub[x]:
            os.rename(sub[x], 'HU_0.nii')
        elif "HU_0.nii" in sub[x]:
            os.system("/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/automated_scripts/nii2png.py -i " + sub[x] + " -o " + path_new_jpeg + "")
            
