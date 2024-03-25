import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

def degToCompass(degrees):
    """
    Description: Convert degrees to compass direction
    
    Input: degrees (int) - the degree value
    
    Output: direction (str) - the compass direction
    """
    val = int((degrees/22.5)+.5)
    directions = ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return directions[(val % 16)]

# Path for work computer
# path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\pm_data_epa\flint_data.csv"

# Path for laptop
# path = r"S:\CHM\ExposureScienceLab\Flint Maternal Health Study\windrose\pm_data_epa\flint_data.csv"

# ---------------------- PM Data ---------------------- #
# New dataset downloaded from https://aqs.epa.gov/aqsweb/airdata/download_files.html
# MI state code: 26
# Genesse county code: 49
# Site num - 420 East Boulevard Drive: 11 (NOT USED IN PM DATA, WAS JUST LISTED IN SITE DESCRIPTION DATA)
# Site num - Whaley PK 3610 IOWA: 21
# units are in ug/m3
pm_path = r"S:\CHM\ExposureScienceLab\Flint Maternal Health Study\windrose\pm_data_epa\hourly_88101_2023.csv"
# ----------------------------------------------------- #

# ---------------------- Wind Data ---------------------- #
# Also downloaded from the same website, under hourly category, then wind
# 1 knot is about 0.514444 m/s
wind_path = r"S:\CHM\ExposureScienceLab\Flint Maternal Health Study\windrose\wind_data_epa\hourly_WIND_2023.csv"
# ----------------------------------------------------- #

# using this bc vpn make it slow
tmp_pm_path = r"C:\Users\tuann\Downloads\hourly_88101_2023\hourly_88101_2023.csv"
# tmp_wind_path = r"C:\Users\tuann\Downloads\hourly_WIND_2023\hourly_WIND_2023.csv"
tmp_wind_path = r"C:\Users\tuann\github\esl_scripts\data\wind_rose_test.csv"

cols = ['State Code','County Code',
        'State Name','County Name',
        'Site Num','Parameter Name', # check if there are other parameter names besides PM2.5
        'Latitude','Longitude',
        'Date Local','Time Local',
        'Sample Measurement','Units of Measure'
        ]

# read in data
pm_dat = pd.read_csv(tmp_pm_path, usecols=cols)
wind_data = pd.read_csv(tmp_wind_path, usecols=cols)

# filter data
pm_dat = pm_dat[(pm_dat['State Code'] == 26) & (pm_dat['County Code'] == 49) & (pm_dat['Site Num'] == 21)]
#wind_data = wind_data[(wind_data['State Code'] == 26) & (wind_data['County Code'] == 49)]
wind_data = wind_data[(wind_data['State Code'] == 26) & (wind_data['County Code'] == 49) & (wind_data['Site Num'] == 21)]
wind_dir_data = wind_data[wind_data['Parameter Name'] == 'Wind Direction - Resultant']
wind_speed_data = wind_data[wind_data['Parameter Name'] == 'Wind Speed - Resultant']

# print(wind_data['Parameter Name'].unique())
# pm_dat.columns
# print(pm_dat.head())
print(wind_data.head())
print(wind_dir_data)
print(wind_speed_data)

# ---------------------- PM data work ---------------------- #
# pm_dat['Date Local'] = pd.to_datetime(pm_dat['Date Local'])
pm_dat['Sample Measurement'] = pd.to_numeric(pm_dat['Sample Measurement'], errors='coerce')
pm_dat['Sample Measurement'] = pm_dat['Sample Measurement'].fillna(0)
pm_dat['Sample Measurement'] = pm_dat['Sample Measurement'].astype(float)

pm_dat_daily = pm_dat[['Date Local','Sample Measurement']]
pm_dat_daily = pm_dat_daily.groupby('Date Local').mean()
print(pm_dat_daily)
# ----------------------------------------------------- #

# ---------------------- Wind data work ---------------------- #
# wind_dir_data['Date Local'] = pd.to_datetime(wind_dir_data['Date Local'])
# wind_dir_data['Time Local'] = pd.to_datetime(wind_dir_data['Time Local'], format='%H:%M')
# wind_speed_data['Date Local'] = pd.to_datetime(wind_speed_data['Date Local'])
# wind_speed_data['Time Local'] = pd.to_datetime(wind_speed_data['Time Local'], format='%H:%M')

wind_dir_data_daily = wind_dir_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]
wind_speed_data_daily = wind_speed_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]

# print(wind_dir_data_daily['Time Local'])
# print(wind_dir_data_daily['Date Local'])
# print(wind_speed_data_daily['Time Local'])
# print(wind_speed_data_daily['Date Local'])

# convert knots to m/s
#print(wind_speed_data_daily['Sample Measurement'])
# wind_speed_data_daily.loc[:, 'Sample Measurement'] = wind_speed_data_daily['Sample Measurement'] * 0.514444
#print(wind_speed_data_daily['Sample Measurement'].astype(int)) 

iter_counter = 0
for date in wind_dir_data_daily['Date Local'].unique():
    
    # combine the wind direction and wind speed data for that date and time
    wind_dir = wind_dir_data_daily[wind_dir_data_daily['Date Local'] == date]
    print(f"unique num of hours for dir: {len(wind_dir['Time Local'].unique())}")
    print(f"total num of hours for dir: {len(wind_dir['Time Local'])}")
    
    wind_speed = wind_speed_data_daily[wind_speed_data_daily['Date Local'] == date] 
    print(f"unique num of hours for dir: {len(wind_speed['Time Local'].unique())}")
    print(f"total num of hours for dir: {len(wind_speed['Time Local'])}")
    wind_data_daily = pd.merge(wind_dir, wind_speed, on='Time Local')
    
    # drop unnecessary columns
    wind_data_daily = wind_data_daily.drop(columns=['Date Local_y'])
    len(wind_data_daily)
    random_indexes = np.random.randint(0, 23, 3)
    print(f"random indexes to be checked: {random_indexes}")
    
    print(wind_data_daily)
    
    try:
        for i in random_indexes:
            if i > (len(wind_data_daily) - 1):
                i = len(wind_data_daily) - 1
            print(f"index being checked: {i}")
            wind_data_daily_row = wind_data_daily.loc[i]
            print(f"wind_data_daily row {i}\n{wind_data_daily_row}")
            date_to_check = wind_data_daily_row['Date Local_x']
            time_to_check = wind_data_daily_row['Time Local']
            wind_dir_to_check = float(wind_data_daily_row['Sample Measurement_x'])
            wind_speed_to_check = wind_data_daily_row['Sample Measurement_y']
            direction_in_raw_data = float(wind_dir_data[(wind_dir_data['Date Local'] == date_to_check) & (wind_dir_data['Time Local'] == time_to_check)]['Sample Measurement'].iloc[0])
            speed_in_raw_data = float(wind_speed_data[(wind_speed_data['Date Local'] == date_to_check) & (wind_speed_data['Time Local'] == time_to_check)]['Sample Measurement'].iloc[0])
            #speed_in_raw_data = speed_in_raw_data * 0.514444
            
            if direction_in_raw_data == wind_dir_to_check:
                print('Wind direction is correct')
                print(f"""Date: {date_to_check}, Time: {time_to_check}\nWind speed in raw data: {direction_in_raw_data}\nWind speed in processed data: {wind_dir_to_check}""")
            else:
                print('Wind direction is incorrect')
                print(f"""Date: {date_to_check}, Time: {time_to_check}\nWind speed in raw data: {direction_in_raw_data}\nWind speed in processed data: {wind_dir_to_check}""")
                break
            if speed_in_raw_data == wind_speed_to_check:
                print('Wind speed is correct')
                print(f"""Date: {date_to_check}, Time: {time_to_check}\nWind speed in raw data: {speed_in_raw_data}\nWind speed in processed data: {wind_speed_to_check}""")
                
            else:
                print('Wind speed is incorrect')
                print(f"""Date: {date_to_check}, Time: {time_to_check}\nWind speed in raw data: {speed_in_raw_data}\nWind speed in processed data: {wind_speed_to_check}""")
                break
    except Exception as e:
        print(e)
    
    # now need to get x and y components of wind velocity based on speed and direction
    # x = speed * cos(direction)
    # y = speed * sin(direction)
    # Sample Measurement_x is the wind direction
    # Sample Measurement_y is the wind speed
    # VelX = Mag * Cos(2 * pi * (90 - Dir) / 360) # formula from excel sheet
    # VelY = Mag * Sin(2 * pi * (90 - Dir) / 360) # formula from excel sheet
    
    # weighted velocity is coming out right ########################################    
    wind_data_daily['x_component'] = wind_data_daily['Sample Measurement_y'] * np.cos(2 * np.pi * (90 - wind_data_daily['Sample Measurement_x']) / 360)
    wind_data_daily['y_component'] = wind_data_daily['Sample Measurement_y'] * np.sin(2 * np.pi * (90 - wind_data_daily['Sample Measurement_x']) / 360)
    
    mean_x_component = wind_data_daily['x_component'].mean()
    print(f"Mean x component: {mean_x_component}")
    mean_y_component = wind_data_daily['y_component'].mean()
    print(f"Mean y component: {mean_y_component}")
    
    weighted_velocity = np.sqrt(mean_x_component**2 + mean_y_component**2)
    print(f"Weighted velocity: {weighted_velocity}")
    ################################################################################
    
    # weighted directiion is not coming out right
    def PolarCoord(x, y):
        if x == 0 and y == 0:
            return 0
        elif x == 0 and (y > 0 or y < 0):
            rAlpha = 90 - ((y/y)*90)
            return rAlpha
        else:
            rAlpha = (180 / np.pi * np.arctan(x / y)) # + 360
            return rAlpha
    weighted_direction = PolarCoord(mean_x_component, mean_y_component)
    print(f"weighted direction: {weighted_direction}")
    weighted_direction_str = degToCompass(weighted_direction)
    print(f"weighted direction str: {weighted_direction_str}")
    
    iter_counter += 1
    if iter_counter < 3:
        # print(wind_data_daily)
        continue
    else:
        break
# ----------------------------------------------------- #
