#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 12:15:58 2021

@author: komal
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 12:16:02 2021

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
import pathlib
import datetime

Voxel_Size, Scan_Date, Scan_Time, Dimensions, Offset, Matrix_Size, Slices,name, Dynamics = [],[],[],[],[],[],[],[], []
direc="/media/komal/DATA00/Komal_all/FMRI_QC_final_200921/sample_fmri_data/*"
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    name.append(os.path.basename(folder[z]))
    l=0
    sub = sorted(glob.glob(folder[z]+"/*")) 
    for x in range(len(sub)):
        if "SENSE" in sub[x]:      
            Num = list()
            slices1=list()
            dyn1 = list()
            img = nib.load(sub[x])
            hdr = img.header
            voxel_size1= hdr.get_zooms()
            vox = voxel_size1[0:3]
            voxel_size  ='X'.join([str(i) for i in vox])
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
            dyn1.append(dimensions1[3])
            dynamics ='X'.join([str(i) for i in dyn1])
            fname = pathlib.Path(sub[x])
            assert fname.exists(), f'No such file: {fname}'
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
            Dynamics.append(dynamics)
import xlsxwriter
workbook = xlsxwriter.Workbook('/home/komal/django-apps/testsite/acquisition_param_fMRI.xlsx', {'nan_inf_to_errors':True})
worksheet = workbook.add_worksheet()
iqm = {'Subject_ID': name,'Voxel Size': Voxel_Size, 'Scan Date': Scan_Date, 'Scan Time': Scan_Time, 'Offset': Offset, 'Matrix':Matrix_Size, 'Slices': Slices, 'Dynamics': Dynamics}
col_num = 0
for key, value in iqm.items():
    worksheet.write(0, col_num, key)
    worksheet.write_column(1,col_num, value)
    col_num +=1
workbook.close()
import pandas as pd
read_file = pd.read_excel ("/home/komal/django-apps/testsite/acquisition_param_fMRI.xlsx")
read_file.to_csv ("/home/komal/django-apps/testsite/acquisition_param_fMRI.csv", 
                  index = None,
                  header=True)





# direc="/home/komal/django-apps/testsite/QC_folder/*"
# folder = sorted(glob.glob(direc))
# for z in range(len(folder)):
#     if "HU" in folder[z]:
#         sub = sorted(glob.glob(folder[z]+"/*"))
#         for x in range(len(sub)):
#             dirpath = (folder[z]+"/")
#             os.chdir(dirpath)
#             if "HU" in sub[x]:
#                 os.rename(sub[x], 'HU_0.nii')
# from nibabel.testing import data_path
# example_filename = os.path.join(data_path, '/home/komal/Desktop/HU2693_PRAVAT_01_11_20_WIP_IBT_sT1W_3D_SENSE_3_1.nii')
# img = nib.load(example_filename)
# filename= img.from_filename('/home/komal/Desktop/HU2693_PRAVAT_01_11_20_WIP_IBT_sT1W_3D_SENSE_3_1.nii')
# hdr = img.header
# print(img)
# print(type(hdr))

# filetype = img.files_types
# shape = img.shape
# pixel_size = hdr.get_zooms()

# #FOV = list[shape[0], shape[1]]
# objects= img.dataobj
# dimensions = hdr.get_data_shape()
# Num = list()
# Num.append(dimensions[0])
# Num.append(dimensions[1])
# slices=list()
# slices.append(dimensions[2])
# extens = hdr.extensions
# offset = hdr.single_vox_offset

# dimesnsions = hdr._get_checks()





# import pathlib
# fname = pathlib.Path('/media/komal/DATA00/Komal_all/MRI_all/mri_qc/data_100/00_InputImages/00_InputImages/001_T1_T1w.nii')
# assert fname.exists(), f'No such file: {fname}'  # check that the file exists
# import datetime
# Scan_date = datetime.datetime.fromtimestamp(fname.stat().st_mtime).date()
# St = datetime.datetime.fromtimestamp(fname.stat().st_mtime).time()
# scan_time = St.isoformat()
# #Scan_date = mtime.datetime.datetime.now().date()












