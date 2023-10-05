# MSU Exposure Science Lab Script Usage
Doc creator: Tuan N.

## Description
This document contains instructions for running various scripts for data extraction, analysis and visualization.

## Scripts Available
**pdr_summary_stats_rlde.py**
- This script calculates summary stats for PM2.5 measured by pDRs. Note that this is specifically for the RLDE project, and relies on a specific naming convention and file structure.
- *Instructions:*
	1. Download the data.
		a. [Download data off pDR instructions]
	2. Move the files to 'S:\ExposureScienceLab\Lead Dust\Data\pDR\new_files'
	3. Open command prompt, type 'python path\to\pdr_summary_stats_rlde.py' without the ' and then press enter.
	4. Files will be saved in respective subject folder.
- *Example:*
	- python C:\Users\nguye620\esl_scripts\pdr_summary_stats_rlde.py

**pdr_summary_stats_general.py**
- This script is for general usage, and will calculate summary stats for files in the 'C:\Users\nguye620\esl_scripts\input' directory
- Users may also specify input and output directories with the '-i' and '-o' options respectively.
- *Instructions:*
	1. Download the data.
	2. Move the files to 'C:\Users\nguye620\esl_scripts\input'
	3. Open command prompt, type 'python path\to\pdr_summary_stats_general.py' and then press enter.
	4. Files will be saved in 'C:\Users\nguye620\esl_scripts\input'
- *Example without specific directories:*
	- python C:\Users\nguye620\esl_scripts\pdr_summary_stats_general.py
- *Example with specific directories:*
	- python C:\Users\nguye620\esl_scripts\pdr_summary_stats_general.py -i "S:\ExposureScienceLab\2_RAPIDS\pDR Data\pDR 9\Subject 40" -o "S:\ExposureScienceLab\2_RAPIDS\pDR Data\pDR 9\Subject 40"
- *Notes:*
	- When using the '-i' and '-o' options, the path may have to have quotation marks in the beginning and end.

**pa_data_processing_cwf.py**
- aaa

**pa_data_processing_general.py**
- aaa