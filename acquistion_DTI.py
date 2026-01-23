#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 12:17:01 2021

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

Voxel_Size, Scan_Date, Scan_Time, Dimensions, Offset, Matrix_Size, Slices,name = [],[],[],[],[],[],[],[]
direc="/home/komal/django-apps/testsite/media/DTI/*"
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
import xlsxwriter
workbook = xlsxwriter.Workbook('/home/komal/django-apps/testsite/acquisition_param.xlsx', {'nan_inf_to_errors':True})
worksheet = workbook.add_worksheet()
iqm = {'Subject_ID': name,'Voxel Size': Voxel_Size, 'Scan Date': Scan_Date, 'Scan Time': Scan_Time, 'Dimensions': Dimensions, 'Offset': Offset, 'Matrix':Matrix_Size, 'Slices': Slices }
col_num = 0
for key, value in iqm.items():
    worksheet.write(0, col_num, key)
    worksheet.write_column(1,col_num, value)
    col_num +=1
workbook.close()
import pandas as pd
read_file = pd.read_excel ("/home/komal/django-apps/testsite/acquisition_param.xlsx")
read_file.to_csv ("/home/komal/django-apps/testsite/acquisition_param.csv", 
                  index = None,
                  header=True)
