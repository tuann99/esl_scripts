# MSU Exposure Science Lab Script Usage
**Doc creator:** Tuan N.

## Description
This document contains instructions for running various scripts for data extraction, analysis, and visualization.

## Scripts Available
### pdr_summary_stats_rlde.py
- This script calculates summary stats for PM2.5 measured by pDRs. Note that this is specifically for the RLDE project and relies on a specific naming convention and file structure.
- **Instructions:**
   1. Download the data.
      - [Download data off pDR instructions]
   2. Move the files to 'S:\ExposureScienceLab\Lead Dust\Data\pDR\new_files'.
   3. Open the command prompt, type the following command, and press enter.
      ```shell
      python path\to\pdr_summary_stats_rlde.py
      ```
   4. Files will be saved in respective subject folders.
- **Example:**
   - ```shell
     python C:\Users\nguye620\esl_scripts\pdr_summary_stats_rlde.py
     ```

### pdr_summary_stats_general.py
- This script is for general usage and calculates summary stats for files in the 'C:\Users\user_name\esl_scripts\input' directory.
- Users can specify input and output directories with the '-i' and '-o' options, respectively.
- **Instructions:**
   1. Download the data.
   2. Move the files to 'C:\Users\user_name\esl_scripts\input'.
   3. Open the command prompt, type the following command, and press enter.
   4. Files will be saved in 'C:\Users\user_name\esl_scripts\output'.
- **Example without specific directories:**
   - ```shell
     python C:\Users\nguye620\esl_scripts\pdr_summary_stats_general.py
     ```
- **Example with specific directories:**
   - ```shell
     python C:\Users\nguye620\esl_scripts\pdr_summary_stats_general.py -i "S:\ExposureScienceLab\2_RAPIDS\pDR Data\pDR 9\Subject 40" -o "S:\ExposureScienceLab\2_RAPIDS\pDR Data\pDR 9\Subject 40"
     ```
- **Notes:**
   - When using the '-i' and '-o' options, the path may need to be enclosed in quotation marks.

### pa_data_processing_cwf.py
- aaa

### pa_data_processing_general.py
- aaa