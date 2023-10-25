# MSU Exposure Science Lab Scripts
**Creator:** Tuan N.

## Description
This document contains instructions for running various scripts for data extraction, analysis, and visualization. Users should clone the repo to 
'C:\Users\user_name\' to be able to use the scripts as they are.

## Scripts Available
### pdr_summary_stats_rlde.py
- **Description:**
   - This script calculates summary stats for PM2.5 measured by pDRs. Note that this is specifically for the RLDE project and relies on a specific naming convention and file structure.
- **Requirements:**
   - Python
   - Modules:
- **Instructions:**
   1. Download the data from the pDR. Refer to the SOP in 'Lab Protocols' for full instructions.
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
- **Description:**
   - This script is for general usage and calculates summary stats for files in the 'C:\Users\user_name\esl_scripts\input' directory.
   - Users can specify input and output directories with the '-i' and '-o' options, respectively.
- **Requirements:**
   - Python
   - Modules:
- **Instructions:**
   1. Download the data.
   2. If using the default directories, move the files to 'C:\Users\user_name\esl_scripts\input'. Else, move to step 3.
   3. Open the command prompt, type the following command, and press enter.
   - ```shell
      python C:\Users\user_name\esl_scripts\pdr_summary_stats_general.py
      ```
   - 'user_name' should be filled in with user's username. This can be found by typing into command prompt 'whoami'
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
- **Description:**
- **Requirements:**
- **Instructions:**
- **Example:**

### pa_data_processing_general.py
- **Description:**
- **Requirements:**
- **Instructions:**
- **Example:**

### rlde_data_analysis.py
- **Description:**
- **Requirements:**
- **Instructions:**
- **Example:**

### rlde_dw_graph.py
- **Description:**
- **Requirements:**
- **Instructions:**
- **Example:**

### rlde_pdr_graph.py
- **Description:**
- **Requirements:**
- **Instructions:**
- **Example:**