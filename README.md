# MSU Exposure Science Lab Scripts
**Creator:** Tuan N.

## Description
This is a repo for scripts used in the lab for tasks such as data management and visualization.

## Scripts Available
### ```create_emissions_map.py```
- **Description**
   - This script creates an interactive map of emission sites from ```xlsx``` files downloaded from the Environmental Protection Agency's (EPA) [National Emissions Inventory (NEI) data retrieval tool](https://www.epa.gov/air-emissions-inventories/2020-national-emissions-inventory-nei-data).
- **Output**
   - HTML file containing the map.
- **Requirements**
   - Python
   - Modules: Available inside ```/venv_requirements/emissions-map-env-requirements.txt```
   - An ```xlsx``` file with the following columns: 'SITE NAME', 'Facility Type', 'Emissions (Tons)', 'Latitude', 'Longitude', 'State-County'
- **Instructions**
   1. Download the data from the EPA NEI as an ```xlsx``` file.
   2. Note the path the data was downloaded to.
   3. Open the command prompt, and type ```python path/to/create_emissions_map.py -i <input_xlsx_path> -o <output_dir>```, where ```path/to/create_emissions_map.py``` is the path to the ```create_emissions_map.py``` script, ```<input_xlsx_path>``` is the path to the EPA NEI data, and ```<output_dir>``` is the directory you want the output ```html``` file to be saved.
- **Example**
```python .\create_emissions_map.py -i "C:\Users\nguye620\esl_scripts\input\Kent Facility Data Emissions.xlsx" -o C:\Users\nguye620\esl_scripts\output -c "MI - Kent"```
- **Notes**
   - If "Usecols do not match columns, columns expected but not found: ['SITE NAME'] (sheet: 0)" error occurs, open the xlsx file and ensure the column name for site name has only one space between SITE and NAME (i.e. 'SITE NAME', not 'SITE  NAME')

### ```create_trap_risk_map.py```
- **Description**
   - This script creates a map that contains 500, 300, 150 meter buffers around state-owned roads.
- **Output**
   - HTML file containing the map.
- **Requirements**
   - Python
   - Modules: Available inside ```/venv_requirements/trap-map-env.txt```
   - Data 
- **Instructions**
   1. Download the data from the EPA NEI as an ```xlsx``` file.
   2. Note the path the data was downloaded to.
   3. Open the command prompt, and type ```python path/to/create_emissions_map.py -i <input_xlsx_path> -o <output_dir>```, where ```path/to/create_emissions_map.py``` is the path to the ```create_emissions_map.py``` script, ```<input_xlsx_path>``` is the path to the EPA NEI data, and ```<output_dir>``` is the directory you want the output ```html``` file to be saved.
- **Example**
```python .\create_trap_risk_map.py -lat -i "C:\Users\nguye620\esl_scripts\input\Kent Facility Data Emissions.xlsx" -o C:\Users\nguye620\esl_scripts\output -c "MI - Kent"```
- **Notes**
   - If "Usecols do not match columns, columns expected but not found: ['SITE NAME'] (sheet: 0)" error occurs, open the xlsx file and ensure the column name for site name has only one space between SITE and NAME (i.e. 'SITE NAME', not 'SITE  NAME')

### ```pdr_summary_stats_rlde.py```
- **Description**
   - This script calculates summary stats for PM2.5 measured by pDRs. Note that this is specifically for the RLDE project and relies on a specific naming convention and file structure.
- **Requirements**
   - Python
   - Modules:
- **Instructions**
   1. Download the data from the pDR. Refer to the SOP in 'Lab Protocols' for full instructions.
   2. Move the files to 'S:\ExposureScienceLab\Lead Dust\Data\pDR\new_files'.
   3. Open the command prompt, type ```python path\to\pdr_summary_stats_rlde.py```, and press enter.
   4. Files will be saved in respective subject folders.
- **Example**
```shell
python C:\Users\nguye620\esl_scripts\pdr_summary_stats_rlde.py
```

### ```pdr_summary_stats_rlde.py```
- **Description**
   - This script calculates summary stats for PM2.5 measured by pDRs. Note that this is specifically for the RLDE project and relies on a specific naming convention and file structure.
- **Requirements**
   - Python
   - Modules:
- **Instructions**
   1. Download the data from the pDR. Refer to the SOP in 'Lab Protocols' for full instructions.
   2. Move the files to 'S:\ExposureScienceLab\Lead Dust\Data\pDR\new_files'.
   3. Open the command prompt, type ```python path\to\pdr_summary_stats_rlde.py```, and press enter.
   4. Files will be saved in respective subject folders.
- **Example**
```shell
python C:\Users\nguye620\esl_scripts\pdr_summary_stats_rlde.py
```

### ```pdr_summary_stats_general.py```
- **Description**
   - This script is for general usage and calculates summary stats for files in the 'C:\Users\user_name\esl_scripts\input' directory.
   - Users can specify input and output directories with the '-i' and '-o' options, respectively.
- **Requirements**
   - Python
   - Modules:
- **Instructions**
   1. Download the data.
   1. If using the default directories, move the files to ```C:\Users\user_name\esl_scripts\input```. Else, move to step 3.
   1. Open the command prompt, type ```python C:\Users\user_name\esl_scripts\pdr_summary_stats_general.py```, and press enter.
*Note: 'user_name' should be filled in with user's username. This can be found by typing into command prompt 'whoami'*
   1. Files will be saved in ```C:\Users\user_name\esl_scripts\output```.
- **Example without specific directories**
   - ```shell
     python C:\Users\nguye620\esl_scripts\pdr_summary_stats_general.py
     ```
- **Example with specific directories**
   - ```shell
     python C:\Users\nguye620\esl_scripts\pdr_summary_stats_general.py -i "S:\ExposureScienceLab\2_RAPIDS\pDR Data\pDR 9\Subject 40" -o "S:\ExposureScienceLab\2_RAPIDS\pDR Data\pDR 9\Subject 40"
     ```
- **Notes**
   - When using the '-i' and '-o' options, the path may need to be enclosed in quotation marks.

### ```pa_data_processing_cwf.py```
- **Description**
- **Requirements**
- **Instructions**
- **Example**

### ```pa_data_processing_general.py```
- **Description**
- **Requirements**
- **Instructions**
- **Example**

### ```rlde_data_analysis.py```
- **Description**
- **Requirements**
- **Instructions**
- **Example**

### ```rlde_dw_graph.py```
- **Description:**
- **Requirements:**
- **Instructions:**
- **Example:**

### ```rlde_pdr_graph.py```
- **Description**
- **Requirements**
- **Instructions**
- **Example**
