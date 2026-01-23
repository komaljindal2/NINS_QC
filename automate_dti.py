#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 11:10:21 2021

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
def correlation_coefficient(patch1, patch2):
    product = np.mean((patch1 - patch1.mean()) * (patch2 - patch2.mean()))
    stds = patch1.std() * patch2.std()
    if stds == 0:
        return 0
    else:
        product /= stds
        return product
    

## Rename the files to make it same for all folders
direc="/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/DTI/*"
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    path_convert =folder[z]
    print(path_convert)
    os.system('dcm2niix '+ path_convert)
    sub = sorted(glob.glob(folder[z]+"/*"))
    for x in range(len(sub)):
        dirpath = (folder[z]+"/")
        os.chdir(dirpath)
        if "ADC.nii" in sub[x]:
            os.remove(sub[x])
        elif ".nii" in sub[x]:
            os.rename(sub[x], 'HU_noeddy0.nii')
        elif ".bval" in sub[x]:
            os.rename(sub[x], 'bval.bval')
        elif ".bvec" in sub[x]:
            os.rename(sub[x], 'bvec.bvec')
            
                
            # elif "dti_ADC" in sub[x]:
            #     os.rename(sub[x], 'HU_ADC.nii')
                
                
                
                
## eddy current correction for each HU_0.nii file in folder 
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    sub = sorted(glob.glob(folder[z]+"/*")) 
    for x in range(len(sub)):
        dirpath = (folder[z]+"/")
        os.chdir(dirpath)
        os.system('eddy_correct HU_noeddy0.nii HU_0.nii 0')
## mask generation for HU_0.nii  file in folder
                
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    sub = sorted(glob.glob(folder[z]+"/*")) 
    for x in range(len(sub)):
        dirpath = (folder[z]+"/")
        os.chdir(dirpath)
        mask=BET(in_file='HU_0.nii.gz', functional=True, mask=True)
        res=mask.run()
            
            
## dtifit for diffusion tensor model fit on dti image to generate analysis files
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    dirpath = (folder[z]+"/")
    os.chdir(dirpath)
    os.system('dtifit -k HU_0.nii.gz -o dti -m HU_0_brain_mask.nii.gz -r bvec.bvec -b bval.bval --sse --save_tensor')
        
        
        
folder = sorted(glob.glob(direc))
std_diff, name, max_z, krt, corr, table_std_sse = [], [], [], [], [], []
for z in range(len(folder)):
    name.append(os.path.basename(folder[z]))
    sub = sorted(glob.glob(folder[z]+"/*"))
    for x in range(len(sub)):
        if "dti_L1.nii.gz" in sub[x]:
            L1=sub[x]
            L1_img = nib.load(L1)
            L1_data = L1_img.get_fdata()
                
        if "dti_L2.nii.gz" in sub[x]:
            L2=sub[x]
            L2_img = nib.load(L2)
            L2_data = L2_img.get_fdata()
            
        if "dti_L3.nii.gz" in sub[x]:
            L3=sub[x]
            L3_img = nib.load(L3)
            L3_data = L3_img.get_fdata()

            mn_data=np.zeros(L1_data.shape)
            fa=np.zeros(L1_data.shape)
            ci=  np.zeros(L1_data.shape) 
            for i in range(len(L1_data[:,1,1])):          
                for j in range(len(L1_data[1,:,1])):
                    for k in range(len(L1_data[1,1,:])):
                        mn_data[i,j,k] = (L1_data[i,j,k]+ L2_data[i,j,k]+ L3_data[i,j,k])/3
            for i in range(len(L1_data[:,1,1])):          
                for j in range(len(L1_data[1,:,1])):
                    for k in range(len(L1_data[1,1,:])): 
                        if (L1_data[i,j,k] !=0 and L2_data[i,j,k] !=0 and L3_data[i,j,k] !=0 and mn_data[i,j,k]<= 0.0018):
                            fa[i,j,k] = (np.sqrt((np.square(L1_data[i,j,k]-mn_data[i,j,k])+np.square(L2_data[i,j,k]-mn_data[i,j,k]))+np.square(L3_data[i,j,k]-mn_data[i,j,k])))/(np.sqrt(np.square(L1_data[i,j,k])+np.square(L2_data[i,j,k])+np.square(L3_data[i,j,k])))
                            ci[i,j,k] = (L1_data[i,j,k]-L2_data[i,j,k])/(np.sqrt(np.square(L1_data[i,j,k])+np.square(L2_data[i,j,k])+np.square(L3_data[i,j,k])))

            wm=np.zeros(fa.shape)
            gm=np.zeros(fa.shape)


            for i in range(len(fa[:,1,1])):          
                for j in range(len(fa[1,:,1])):
                    for k in range(len(fa[1,1,:])):
                        if fa[i,j,k]>0.2:
                            wm[i,j,k]=10*fa[i,j,k]
                        else:
                            gm[i,j,k]=10*fa[i,j,k]
            mean_fa=np.empty(wm[1,1,20:60].shape)
                
            for k in range(len(wm[1,1,20:60])):
                mean_fa[k]=np.mean(np.square(wm[:,:,k+20]))
            st_wm=(np.std(mean_fa))
            list_with_diff = []
            for n in range(1, len(mean_fa)):
                list_with_diff.append(mean_fa[n] - mean_fa[n-1])
        if "dti_sse.nii.gz" in sub[x]:
            sse=sub[x]
            sse_img = nib.load(sse)
            sse_data = sse_img.get_fdata()
            std_v1 = np.zeros(sse_data[1,1,:].shape)
            for i in range(len(sse_data[1,1,:])):          
                std_v1=np.std(sse_data[:,:,i])
               
        if "HU_0.nii" in sub[x]:
            org=sub[x]
            org_img=nib.load(org)
            org_data = org_img.get_fdata()
            mask=os.path.join(folder[z], 'HU_0_brain_mask.nii.gz')
            mask_img = nib.load(mask)
            mask_data = mask_img.get_fdata()
            mn_xdir=np.zeros(org_data[1,1,:,1].shape)
            for i in range(len(org_data[1,1,:,1])):          
                mn_xdir[i]=np.mean(org_data[:,:,i,:])
            roi_orig=np.zeros(org_data.shape)
            background_orig=np.empty(org_data.shape)
            for i in range(len(org_data[:,1,1,1])):          
                for j in range(len(org_data[1,:,1,1])):
                    for k in range(len(org_data[1,1,:,1])):
                        for l in range(len(org_data[1,1,1,:])):
                            if mask_data[i,j,k]!= 1:
                                background_orig[i,j,k,l] =org_data[i,j,k,l]
                            else:
                                roi_orig[i,j,k,l] =org_data[i,j,k,l]       
            num_sli=[]
            for k in range(len(org_data[1,1,:,1])):
                if k != 69:
                    num_sli.append(correlation_coefficient(org_data[:,:,k,:], org_data[:,:,k+1,:]))
            com_x=np.zeros(roi_orig[1,:,:,:].shape)
    path='/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/DTI'
    fileno = os.path.basename(folder[z])
    os.chdir("/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/DTI/"+fileno+"/")
    std_diff.append(20*math.log10(np.std(np.square(list_with_diff))))
    max_z.append(np.max(mn_xdir))
    krt.append(kurtosis(org_data))
    corr.append(np.mean(num_sli))
    table_std_sse.append(np.std(std_v1))


import xlsxwriter
workbook = xlsxwriter.Workbook('dtireport.xlsx', {'nan_inf_to_errors':True})
worksheet = workbook.add_worksheet()
iqm = {'Subject_ID': name,'Scaled_FA_std':std_diff, 'Max_zdir_mn': max_z, 'Correlation_slices': corr, 'SSE_std':table_std_sse}
col_num = 0
for key, value in iqm.items():
    worksheet.write(0, col_num, key)
    worksheet.write_column(1,col_num, value)
    col_num +=1
workbook.close()

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
import pathlib
import datetime

Voxel_Size, Scan_Date, Scan_Time, Dimensions, Offset, Matrix_Size, Slices,name = [],[],[],[],[],[],[],[]
direc="/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/DTI/*"
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    name.append(os.path.basename(folder[z]))
    l=0
    sub = sorted(glob.glob(folder[z]+"/*")) 
    for x in range(len(sub)):
        if "HU_noeddy0.nii" in sub[x]:      
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
            assert fname.exists()
            Scan_date1 = datetime.datetime.fromtimestamp(fname.stat().st_mtime).date()
            Scan_date = Scan_date1.strftime('%m/%d/%Y')
            St = datetime.datetime.fromtimestamp(fname.stat().st_mtime).time()
            scan_time = St.isoformat()
    Voxel_Size.append(voxel_size)
    Scan_Date.append(Scan_date)
    Scan_Time.append(scan_time)
    Dimensions.append(dimensions)
    Offset.append(offset)
    Matrix_Size.append(num)
    Slices.append(slices)
        
        
import xlsxwriter
workbook = xlsxwriter.Workbook('dti_acquisition_param.xlsx', {'nan_inf_to_errors':True})
worksheet = workbook.add_worksheet()
iqm = {'Subject_ID': name,'Voxel Size': Voxel_Size, 'Scan Date': Scan_Date, 'Scan Time': Scan_Time, 'Dimensions': Dimensions, 'Offset': Offset, 'Matrix':Matrix_Size, 'Slices': Slices }
col_num = 0
for key, value in iqm.items():
    worksheet.write(0, col_num, key)
    worksheet.write_column(1,col_num, value)
    col_num +=1
workbook.close()
import pandas as pd
read_file = pd.read_excel ("dti_acquisition_param.xlsx")
read_file.to_csv ("dti_acquisition_param.csv", 
                  index = None,
                  header=True)


from os import path
direc1="/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/DTI/*"
folder = sorted(glob.glob(direc1))
for z in range(len(folder)):
    sub = sorted(glob.glob(folder[z]+"/*"))
    path_new_jpeg = folder[z] + "/jpeg"
    os.mkdir(path_new_jpeg)
    for x in range(len(sub)):
        if "HU_noeddy0.nii" in sub[x]:
            os.system("med2image -i " + sub[x] + " -d " + path_new_jpeg + " -f 1  --outputFileType png")
            
