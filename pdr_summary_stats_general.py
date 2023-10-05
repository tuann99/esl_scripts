#################################################################################################
#################################################################################################
# Michigan State University - Exposure Science Lab
# Creator: Tuan Nguyen
# Date Created: 2023-10-04
#
# Description:
#  - This is a script for extracting data from the pDR txt files, calculating summary statistics, 
#    and then creating an excel file with the data, summary stats, and chart.
#
# Requirements:
#  - Data should be in .txt format.
#  - Files must include "Subject #" in the file name to move the files to the correct folder.
#  - pDRs must be in the pdr_num_dict dictionary.
#
# Usage:
#  - This script is best used in the command line.
#  - Here is the command to run the script:
#  - python path\to\pdr_summary_stats_general.py -i path\to\input_directory -o path\to\output_directory
#  - "python" allows us to run the script in the command line.
#  - "path\to\pdr_summary_stats_general.py" is the path to the script.
#  - "-i" is the flag for the input directory.
#  - "path\to\input_directory" is the path to directory containing all your files.
#  - "-o" is the flag for the output directory.
#  - "path\to\output_directory" is the path to where you want the files to be output.
# Example:
#  - python S:\ExposureScienceLab\scripts\pdr_summary_stats_general.py -i "S:\ExposureScienceLab\Lead Dust\Data\pDR\new_files" -o "S:\ExposureScienceLab\Lead Dust\Data\pDR"
#
# Notes:
#  - By default, the input directory is "S:\ExposureScienceLab\scripts\input" and the output directory is "S:\ExposureScienceLab\scripts\output".
#################################################################################################
#################################################################################################

import pandas as pd
import os
import argparse
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference 
import shutil

# variables
custom_headers = ["record", "ug/m3", "Temp", "RHumidity", "AtmoPressure", "Flags", "time", "date"]
pdr_num_dict = {
    "0115250158": "pdr_1",
    "0115249628": "pdr_2",
    "0115249629": "pdr_3",
    "0115250156": "pdr_4",
    # pdr 5
    "CM19342019": "pdr_6",
    # pdr 7
    "CM21092015": "pdr_8",
    # pdr 9
}

# start of script
def pdr_summary_stats(input_directory, output_directory):
    for file in os.listdir(input_directory):
        if file.endswith(".txt"):
            
            # first create some file paths and extract some info
            file_path = os.path.join(input_directory, file) # create file path
            print(f"File found at: {file_path}.")
            base_name = os.path.splitext(os.path.basename(file))[0] # extracting name for xlsx file
            print(f"File name is: {base_name}.")

            # copy file to correct subject folder
            shutil.copy2(file_path, output_directory)
            os.chdir(output_directory)

            # create output file paths
            output_txt_path = os.path.join(output_directory, file)
            output_xlsx_path = os.path.join(output_directory, f"{base_name}.xlsx")

            # working w the xlsx file
            workbook = Workbook()

            # open the file and see if there is a serial number, if so, then go ahead with data extraction
            with open(output_txt_path, 'r') as z:
                lines = z.readlines()
                for line in lines: # parse file for serial number by looking for string after "Serial no.  "
                    if "Serial no." in line: # if serial number is found, then go ahead with data extraction
                        serial_num = line.split("Serial no.  \", ")[1].strip().replace('"', '')
                        tmp = pd.read_csv(file_path, sep=",", skiprows=24, header=None, names=custom_headers)
                        tmp["pdr name"] = pdr_num_dict[serial_num]  # add column for pdr name
                        tmp["time"] = tmp["time"].str.strip()  # Remove leading and trailing whitespace
                        tmp["date"] = tmp["date"].str.strip()
                        summary_stats = tmp["ug/m3"].describe() # summary statistics

                        # write thedata to xlsx file in 'Data' sheet
                        data_sheet = workbook.create_sheet(title='Data') # create sheet for data
                        data_sheet.append(custom_headers) # add headers to data sheet
                        for idx, row in tmp.iterrows():
                            data_sheet.append(row.tolist())

                        # write the summary statistics to xlsx file in a new sheet
                        summary_sheet = workbook.create_sheet(title='Summary Statistics') # create sheet for summary statistics
                        summary_stats_list = summary_stats.reset_index().values.tolist()
                        for row in summary_stats_list:
                            summary_sheet.append(row)
                        
                        # create the chart on summary sheet
                        chart = LineChart()
                        chart.title = "ug/m3 Over Time"
                        chart.y_axis.title = "ug/m3"
                        chart.x_axis.title = "Time"
                        y = Reference(data_sheet, min_col=2, min_row=2, max_col=2, max_row=len(tmp) + 1)
                        x = Reference(data_sheet, min_col=7, min_row=2, max_row=len(tmp) + 1)
                        chart.add_data(y, titles_from_data=True)
                        chart.set_categories(x)
                        summary_sheet.add_chart(chart, "A10")

                        # remove the default sheet
                        default_sheet = workbook["Sheet"]
                        workbook.remove(default_sheet)

                        workbook.save(output_xlsx_path)
                        print(f"Data and Summary statistics saved to {output_xlsx_path}")
        if file in os.listdir(output_directory):
            if os.path.getsize(output_xlsx_path) > 0:
                os.remove(file_path)
                print(f"File {file} deleted from {input_directory}.")
            else:
                print(f"File {file} is empty. Please check the file and try again.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract data from pDR txt files, calculate summary statistics, and create excel file with data, summary stats, and chart.")
    parser.add_argument("-i", "--input_directory", type=str, default="S:\\ExposureScienceLab\\scripts\\input", help="The directory containing the pDR txt files.")
    parser.add_argument("-o", "--output_directory", type=str, default="S:\\ExposureScienceLab\\scripts\\output", help="The directory to save the output files to.")
    args = parser.parse_args()
    pdr_summary_stats(args.input_directory, args.output_directory)