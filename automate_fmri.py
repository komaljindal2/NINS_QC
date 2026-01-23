
import math
import numpy as np
import nibabel as nib
import nilearn.image as image
import matplotlib.pyplot as plt
import xlsxwriter
import glob
import os
import nipype.interfaces.spm as spm

from os import path




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

Voxel_Size, Scan_Date, Scan_Time, Dimensions, Offset, Matrix_Size, Slices,name, Dynamics = [],[],[],[],[],[],[],[],[]
direc="/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/fMRI/*"
os.environ['SPM_PATH']='/media/ninslab/DATA1/spm12'
spm.SPMCommand.set_mlab_paths(paths=os.environ['SPM_PATH'])
folder = sorted(glob.glob(direc))
for z in range(len(folder)):
    path_new_jpeg = folder[z] + "/jpeg"
    os.mkdir(path_new_jpeg)
    name.append(os.path.basename(folder[z]))
    l=0
    sub = sorted(glob.glob(folder[z]+"/*")) 
    for x in range(len(sub)):
        if "EPI" in sub[x]:  
            os.system("python3 /home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/automated_scripts/nii2png.py -i " + sub[x] + " -o " + path_new_jpeg + " ")
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
            path='/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/fMRI'
            fileno = os.path.basename(folder[z])
            os.chdir("/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/fMRI/"+fileno+"/")
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
workbook = xlsxwriter.Workbook('fmri_acquisition_param.xlsx', {'nan_inf_to_errors':True})
worksheet = workbook.add_worksheet()
iqm = {'Subject_ID': name,'Voxel Size': Voxel_Size, 'Scan Date': Scan_Date, 'Scan Time': Scan_Time, 'Offset': Offset, 'Matrix':Matrix_Size, 'Slices': Slices, 'Dynamics': Dynamics}
col_num = 0
for key, value in iqm.items():
    worksheet.write(0, col_num, key)
    worksheet.write_column(1,col_num, value)
    col_num +=1
workbook.close()



import pandas as pd
read_file = pd.read_excel ('fmri_acquisition_param.xlsx')
read_file.to_csv ('fmri_acquisition_param.csv', 
                  index = None,
                  header=True)
### The output workbook to be written with all metrics in the excel file.###


workbook = xlsxwriter.Workbook('fmrireport.xlsx')
worksheet = workbook.add_worksheet() 
i=0
worksheet.write(i,0, 'Subject Code')
worksheet.write(i,1, 'Ghost mean')
worksheet.write(i,2, 'Signal mean')
worksheet.write(i,3, 'Background SD') 
worksheet.write(i,4, 'GSR') 
worksheet.write(i,5, 'SNR') 
worksheet.write(i,6, 'tSNR')  
worksheet.write(i,7, 'HM_X')  
worksheet.write(i,8, 'HM_Y')  
worksheet.write(i,9, 'HM_Z')  
worksheet.write(i,10, 'HM_roll')  
worksheet.write(i,11, 'HM_pitch')  
worksheet.write(i,12, 'HM_yaw')  

folders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

for foldername in folders:   
    fPath=os.path.join(path,foldername)
    epi_path= glob.glob(fPath+'/EPI*.nii')
    epi_path = ''.join(str(e) for e in epi_path)
    
    t1_path = glob.glob(fPath+'/T1*.nii')
    t1_path = ''.join(str(e) for e in t1_path)
    
    realign = spm.Realign()
    realign.inputs.in_files = epi_path
    realign.inputs.register_to_mean = True
    realign.run()
    
    realigned_epi_path=glob.glob(fPath+'/rEPI*.nii')
    realigned_epi_path = ''.join(str(e) for e in realigned_epi_path)
    realigned_epi_file=nib.load(realigned_epi_path)
    realigned_epi_data=realigned_epi_file.get_fdata()
    
    mean_epi_path=glob.glob(fPath+'/mean*.nii')
    mean_epi_path = ''.join(str(e) for e in mean_epi_path)
    
    coreg=spm.Coregister()
    coreg.inputs.target = mean_epi_path
    coreg.inputs.source = t1_path
    coreg.run()

    
    cor_t1_path = glob.glob(fPath+'/rT1*.nii')
    cor_t1_path = ''.join(str(e) for e in cor_t1_path)
    
    mean_file=image.mean_img(realigned_epi_file)
    mean_data=mean_file.get_fdata()
    nib.save(mean_file, fPath+'/'+'mean_fmri.nii')
   
    import nipype.interfaces.fsl as fsl
    mybet = fsl.BET()
    result = mybet.run(in_file=cor_t1_path, out_file=fPath+'/output.nii', frac=0.05, surfaces=True)
    mask_file=nib.load(fPath+'/output_outskin_mask.nii.gz')
    mask_data=mask_file.get_fdata()
    
    #head movement
    mot_path = glob.glob(fPath+'/rp_*.txt')
    mot_path = ''.join(str(e) for e in mot_path)
    
    mot=np.loadtxt(mot_path)
    x_dir=(max(mot[:,0])-min(mot[:,0]))
    y_dir=(max(mot[:,1])-min(mot[:,1]))
    z_dir=(max(mot[:,2])-min(mot[:,2]))
                                
    mot_p=mot[:,3]*(180/math.pi)
    mot_r=mot[:,4]*(180/math.pi)
    mot_y=mot[:,5]*(180/math.pi)
    
    pitch=(max(mot_p)-min(mot_p))
    roll=(max(mot_r)-min(mot_r))
    yaw=(max(mot_y)-min(mot_y))
    
    # #Plot
    fig=plt.figure(1)
    plt.subplot(211)
    plt.plot(mot[:,0], label= 'X direction')
    plt.plot(mot[:,1], label='Y direction')
    plt.plot(mot[:,2], label='Z direction')
    plt.xlabel('Dynamics')
    plt.ylabel('mm')
    plt.legend()
    plt.subplot(212)
    plt.plot(mot_p, label= 'Pitch')
    plt.plot(mot_r, label='Roll')
    plt.plot(mot_y, label='Yaw')
    plt.legend()
    plt.xlabel('Dynamics')
    plt.ylabel('degrees')
    # plt.show()
    savepath = os.path.join(fPath, 'HeadMovment.png')
    fig.savefig(savepath)

    # ghost to signal ratio
    RAS_AXIS_ORDER = {'x': 0, 'y': 1, 'z': 2}
    direction="y"
    direction = direction.lower()
    if direction[-1] not in ['x', 'y', 'all']:
        raise Exception("Unknown direction {}, should be one of x, -x, y, -y, all".format(direction))
    axis = RAS_AXIS_ORDER[direction]

    n2_mask = np.roll(mask_data, mask_data.shape[axis] // 2, axis=axis)
    n2_mask_img = nib.Nifti1Image(n2_mask,mask_file.affine)

    n2_mask1 = n2_mask * (1 - mask_data)
    n2_mask1_img = nib.Nifti1Image(n2_mask1,mask_file.affine)

    n2_mask_ng = n2_mask1 + 2 * (1 - n2_mask1 - mask_data)
    n2_mask_ng_img = nib.Nifti1Image(n2_mask_ng,mask_file.affine)
    nib.save(n2_mask_ng_img,fPath+'/'+'n2_mask_ng_img.nii.gz')

    ghost = np.mean(mean_data[n2_mask_ng == 1]) - np.mean(mean_data[n2_mask_ng == 2])
    signal = np.mean(mean_data[n2_mask_ng == 0])
    gsr = float(ghost / signal)

    # Signal to noise ratio
    noise = np.std(mean_data[mask_data == 0])
    snr= float(signal/noise) 
    
    # temporal snr
    noise_tsnr=np.std(realigned_epi_data, axis=3)
    # img = nib.Nifti1Image(noise_tsnr, np.eye(4))
    # nib.save(img,fPath+'/'+'noise_tsnr')
    tsnr_map=np.divide(mean_data,noise_tsnr)
    tsnr_map[np.isnan(tsnr_map)] = 0
    tsnr=np.median(tsnr_map[mask_data == 1])
    
    #mean signal intensity
    size=mean_data.shape;
    x=[]
    s=np.zeros(size[2])
    for x in range(len(mean_data[1,1,:])):
        s[x]=np.mean(mean_data[:,:,x])
        fig=plt.figure(2)
        plt.plot(s)
        plt.xlabel('Slices')
        plt.ylabel('Mean Signal Intensity')
    # plt.show()
        savepath1 = os.path.join(fPath, 'MSI.png')
        fig.savefig(savepath1)
    
    # Use the worksheet object to write data via the write() method. 

    worksheet.write(i+1,0, foldername)
    worksheet.write(i+1,1, round(ghost,4))
    worksheet.write(i+1,2, round(signal,4))
    worksheet.write(i+1,3, round(noise,4)) 
    worksheet.write(i+1,4, round(gsr,4)) 
    worksheet.write(i+1,5, round(snr,4)) 
    worksheet.write(i+1,6, round(tsnr,4)) 
    worksheet.write(i+1,7, round(x_dir,4))
    worksheet.write(i+1,8, round(y_dir,4))
    worksheet.write(i+1,9, round(z_dir,4))
    worksheet.write(i+1,10,round(roll,4))
    worksheet.write(i+1,11,round(pitch,4))
    worksheet.write(i+1,12,round(yaw,4))
      
    i=i+1
    
# Finally, close the Excel file via the close() method. 
workbook.close()


# from os import path
# direc1="/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/QC_folder/fMRI/*"
# folder = sorted(glob.glob(direc1))
# for z in range(len(folder)):
#     sub = sorted(glob.glob(folder[z]+"/*"))
#     path_new_jpeg = folder[z] + "/jpeg"
#     os.mkdir(path_new_jpeg)
#     for x in range(len(sub)):
#         if "EPI.nii" in sub[x]:
#             os.system("med2image -i" + sub[x] + "-d" + path_new_jpeg + " -f 1")
