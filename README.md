The files description is as follows:  \
 The automate_mri.py, automate_fmri.py, automate_dti.py are the quality check scripts to run on folders containing files of MRI, fMRI, DTI respectively.
meta_data files are to extract acquisition parameters for these 3 modalities.
Remaining are the support files.


MRI Quality Control Pipeline
Requirements and Installation Guide

This document outlines all the software packages and dependencies required to run the MRI quality control pipeline script.
System Requirements

    Operating System: Linux (Ubuntu 18.04 or later recommended)

    Python Version: Python 3.6 or higher

    RAM: 8GB minimum (16GB recommended for batch processing)

    Storage: Sufficient space for MRI data processing


    Core Python Packages
Image Processing & Scientific Computing
bash

pip install numpy
pip install scipy
pip install matplotlib
pip install scikit-image
pip install opencv-python
pip install nibabel
pip install pillow

Data Handling & File Operations
bash

pip install pandas
pip install xlsxwriter
pip install openpyxl
pip install glob2

Neuroimaging Tools
bash

pip install nipype

External Software Dependencies
1. FSL (FMRIB Software Library)

Required for BET (Brain Extraction Tool) functionality

Installation:
bash

# Download and install FSL
wget -O- https://fsl.fmrib.ox.ac.uk/fsl/downloads/fslinstaller.py | python

# Or follow the official guide:
# https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation


Verify FSL installation:
bash

which bet

2. SPM12 (Statistical Parametric Mapping)

Required for tissue segmentation

Installation Steps:

    Download SPM12 from: https://www.fil.ion.ucl.ac.uk/spm/software/download/

    Extract to a directory (e.g., /media/ninslab/DATA1/spm12)

    Ensure MATLAB is installed (required for SPM)

Set SPM path in script:
python

os.environ['SPM_PATH'] = '/path/to/your/spm12'

3. MATLAB

Required for SPM12 operation

Installation:

    MATLAB R2017b or newer recommended

    Ensure MATLAB is accessible from command line

4. Additional Scripts

nii2png.py - NIfTI to PNG converter script
The script calls an external conversion tool. Ensure this script exists at:
/home/ninslab/Desktop/Gangotri_15_06_22/django-apps/testsite/automated_scripts/nii2png.py



Directory Structure Requirements

The script expects this directory structure:
text

folder_name/QC_folder/MRI/
├── Subject_1/
│   ├── HU_0.nii
│   └── [other .nii files]
├── Subject_2/
│   ├── HU_0.nii
│   └── [other .nii files]
└── ...
