import pandas as pd
import numpy as np

# Path for work computer
# path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\pm_data_epa\flint_data.csv"

# Path for laptop
path = r"S:\CHM\ExposureScienceLab\Flint Maternal Health Study\windrose\pm_data_epa\flint_data.csv"

cols = ['Latitude', 'Longitude', 'Parameter Name', 'Duration Description', 'Date (Local)', ]
dat = pd.read_csv(path, usecols="Latitude")

# This is the hourly PM data, but have to filter for the flint station
# Idk if the data has it, but on the AirData map, this was the site-id for the Flint station (26-049-0021)
path_2 = r"S:\Users\tuann\Downloads\hourly_88101_2023\hourly_88101_2023.csv"
dat_2 = pd.read_csv(path_2)
dat_2 = dat_2[dat_2['State Name'] == 'Michigan']

print(dat_2.head())
print(dat.head())
