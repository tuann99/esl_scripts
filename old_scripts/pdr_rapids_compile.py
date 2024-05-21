import os
import sys
import pandas as pd
import re
import openpyxl

DATA_DIR = "S:\ExposureScienceLab\RAPIDS\Data\PM2.5\PDR_All_Subjects_fixed"
counter = 0
df = pd.DataFrame()

for file in os.listdir(DATA_DIR):
    counter += 1
    if file.endswith(".xlsx"):
        try:
            file_name_base = str(file)
            print(file_name_base)
            numbers = re.search(r'\d+', file)
            print(numbers)
            if numbers and len(numbers.group()) < 6:
                numbers = numbers.group()
                numbers = numbers.zfill(6)
                print(numbers)
                file_name = f"RAPIDS-P-TEF-{numbers}.xlsx"
                print(file_name)
                # file_path = os.path.join(DATA_DIR, file_name)
                # print(file_path)
                # os.rename(os.path.join(DATA_DIR, file), file_name)
                file_path = os.path.join(DATA_DIR, file)
                
                # add to df
                


        except Exception as e:
            print(e)
            continue
    if counter > 5:
        break

##########################################################################################################

intervention_file = "S:\ExposureScienceLab\RAPIDS\Data\PM2.5\Intervention_PM2_5_Final.xlsx"

with open(intervention_file, "r") as f:
    for i in range(1, 42):
        subject_num = f"Subject{i}"

##########################################################################################################
##########################################################################################################
# TESTING        
##########################################################################################################
##########################################################################################################

wind_file = r"C:\Users\nguye620\Downloads\hourly_WIND_2023\hourly_WIND_2023.csv"
temp_file = r"C:\Users\nguye620\Downloads\hourly_TEMP_2023\hourly_TEMP_2023.csv"
df = pd.read_csv(temp_file, usecols=('State Code', "Site Num", 'Date Local', 'Time Local', 'Sample Measurement'))
df = df[(df['State Code'] == 26) & (df['Site Num'] == 99)]
df = df.reset_index(drop=True)
print(df)
 # now convert YYYY-MM-DD string into YYYYMMDD, and 00:00 24 hour time into whole number (1, 2, 3, ...)
counter = 1
for i in range(0, len(df)+1):
    if i == 0:
        print("length of df is: " + str((len(df)+1)))

    if i == 50:
        break
    print(f"currently on iteration: {i+1}")
        
    # at row i of df['Date Local'], get the date, remove the "-", and replace the date there
    # date = df['Date Local'][i]
    date = df.loc[i, 'Date Local']
    print(f"initial date: {date}")
    date = df.loc[i, 'Date Local'].replace('-', '')
    # date = date.replace('-','')
    print(f"date after replacing: {date}")
    # df['Date Local'][i] = date
    df.loc[i, 'Date Local'] = date
    print(f"date in df: {df.loc[i, 'Date Local']}")

    # Convert 'Time Local' to hour of day as integer
    # then reset the 'Time Local' column to cycle from 1 to 24
    # df['Time Local'] = pd.to_datetime(df['Time Local']).dt.hour + 1
    # df['Time Local'] = df['Time Local'].apply(lambda x: x if x <= 24 else 1)
    
    # using a counter for the whole number hour, and if it goes over 24 hours then reset back to 1
    hour = counter
    print(f"hour: {hour}")
    # df['Time Local'][i] = hour
    df.loc[i, 'Time Local'] = hour
    print(f"here is the hour in the df: {df.loc[i, 'Time Local']}")
    # if counter > 5:
    #     break
    counter += 1
    if counter > 24:
        counter = 1

print(df[0:50])

rh_file = r"C:\Users\nguye620\Downloads\hourly_RH_DP_2023\hourly_RH_DP_2023.csv"
df = pd.read_csv(rh_file)
# df = pd.read_csv(
#     rh_file,
#     usecols=("State Code", "Site Num", 'Latitude', 'Longitude', 'Sample Measurement', 'Units of Measure'))
df = df[(df['State Name'] == 'Michigan')]
df['County Name'].unique()
df = df[(df['County Name'] == 'Wayne')]
df['Site Num'].unique()

df.rename(columns={'Sample Measurement': 'Relative Humidity (%)'}, inplace=True)
df
df = df[(df['Units of Measure'] == 'Percent relative humidity') & (df['State Code'] == 26) & (df['Site Num'] == 14)]
df
df = df.drop(columns='Units of Measure')
df

df.columns
df.head()
df['Units of Measure'].unique()
##########################################################################################################
##########################################################################################################
# TESTING        
##########################################################################################################
##########################################################################################################

# creating functions
import pandas as pd

def create_wind_df(wind_file_path):
    KNOT_TO_KMH_CONVERSION_FACTOR = 1.852
    df = pd.read_csv(
        wind_file_path, 
        usecols=("State Code", "Site Num", 'Latitude', 'Longitude', 'Sample Measurement', 'Units of Measure'))
    df = df[(df['State Code'] == 26) & (df['Site Num'] == 14) & (df['Units of Measure'] == 'Knots')] # nearest place that measured wind speed
    df['Wind Speed (km/h)'] = [speed*KNOT_TO_KMH_CONVERSION_FACTOR for speed in df['Sample Measurement']]
    return df

def create_temp_df(temp_file_path):
    try:
        counter = 1
        df = pd.read_csv(temp_file_path, usecols=('State Code', "Site Num", 'Date Local', 'Time Local', 'Sample Measurement'))
        df = df[(df['State Code'] == 26) & (df['Site Num'] == 99)]
        df.reset_index()
        print(df)
        # now convert YYYY-MM-DD string into YYYYMMDD, and 00:00 24 hour time into whole number (1, 2, 3, ...)
        for i in range(1, len(df) + 1):
            print(f"on iteration: {i}")
            if i == 1:
                print(len(df)+1)
            
            # at row i of df['Date Local'], get the date, remove the "-", and replace the date there
            # date = df['Date Local'][i]
            date = df.loc[i, 'Date Local']
            print(f"initial date: {date}")
            date.replace('-','')
            print(f"date after replacing: {date}")
            # df['Date Local'][i] = date
            df.loc[i, 'Date Local'] = date
            print(f"date that got replaced: {df.loc[i, 'Date Local']}")
        
            # using a counter for the whole number hour, and if it goes over 24 hours then reset back to 1
            hour = counter
            print(f"hour: {hour}")
            # df['Time Local'][i] = hour
            df.loc[i, 'Time Local'] = hour
            print(f"here is the df row: {df.loc[i, 'Time Local']}")

            counter += 1
            if counter > 24:
                counter = 1
        return df
    except Exception as e:
        print(e)
        return e

temp_file = r"C:\Users\nguye620\Downloads\hourly_TEMP_2023\hourly_TEMP_2023.csv"
df = create_temp_df(temp_file)
print(df)
df[0:20]