import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def degToCompass(degrees):
    """
    Description: Convert degrees to compass direction
    
    Input: degrees (int) - the degree value
    
    Output: direction (str) - the compass direction
    """
    val = int((degrees/22.5)+.5)
    directions = ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return directions[(val % 16)]

def direction_to_radians(direction):
    """
    Description: Convert string to radians for position on plot
    
    Input: direction (str) - the direction to be plotted
    
    Output: plot position in radians (int)
    """
    compass = {
        'N': 0,
        'NNE': np.pi/8,
        'NE': np.pi/4,
        'ENE': 3*np.pi/8,
        'E': np.pi/2,
        'ESE': 5*np.pi/8,
        'SE': 3*np.pi/4,
        'SSE': 7*np.pi/8,
        'S': np.pi,
        'SSW': 9*np.pi/8,
        'SW': 5*np.pi/4,
        'WSW': 11*np.pi/8,
        'W': 3*np.pi/2,
        'WNW': 13*np.pi/8,
        'NW': 7*np.pi/4,
        'NNW': 15*np.pi/8
    }
    return compass[direction]

# tmp = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\verification_data\weighted_direction_check.csv"
# dat = pd.read_csv(tmp)
# dat = dat.dropna()
# print(dat)

#      Weighted Direction Direction (blowing from)
# 0            305.210358                       NW
# 2            250.243286                      WSW

# iterate through weighted directions, and compare the actual direction to the 'degToCompass' calculated direction
# iter_counter = 0
# for row in dat.iterrows():
#     weighted_deg = row[1]['Weighted Direction']
#     actual_direction = row[1]['Direction (blowing from)']
#     calculated_direction = degToCompass(weighted_deg)

#     print(f"Weighted direction: {weighted_deg}")
#     print(f"Actual direction: {actual_direction}")
#     print(f"Calculated direction: {calculated_direction}")
#     print("\n")

#     iter_counter += 1

#     if iter_counter > 10:
#         break
#     if actual_direction != calculated_direction:
#         print(f"Weighted direction: {weighted_deg}")
#         print(f"Actual direction: {actual_direction}")
#         print(f"Calculated direction: {calculated_direction}")
#         print("\n")
#     else:
#         continue

def PolarCoord(x, y):
    # pi = np.arctan(1)*4

    if x == 0 and y == 0:
        rAlpha = 0
    elif x == 0 and (y > 0 or y < 0):
        rAlpha = 90 - ((y/y)*90)
    else:
        rAlpha = 360 + (180 / np.pi * np.arctan2(x,y)) # had to swap around to x,y instead of y,x as was in the excel formula

    if rAlpha < 0:
        rAlpha = rAlpha + 360
    elif rAlpha > 360:
        rAlpha = rAlpha - 360
    else:
        rAlpha = rAlpha
    
    return rAlpha

# ---------------------- PM Data ---------------------- #
# New dataset downloaded from https://aqs.epa.gov/aqsweb/airdata/download_files.html
# MI state code: 26
# Genesse county code: 49
# Site num - 420 East Boulevard Drive: 11 (NOT USED IN PM DATA, WAS JUST LISTED IN SITE DESCRIPTION DATA)
# Site num - Whaley PK 3610 IOWA: 21
# units are in ug/m3
#
# Path for laptop
# pm_path = r"S:\CHM\ExposureScienceLab\Flint Maternal Health Study\windrose\pm_data_epa\hourly_88101_2023.csv"
# 
# Path for work computer
pm_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\pm_data_epa\hourly_88101_2023.csv"
pm_ctrl_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\verification_data\pm_verification.csv"
# ----------------------------------------------------- #

# ---------------------- Wind Data ---------------------- #
# Also downloaded from the same website, under hourly category, then wind
# 1 knot is about 0.514444 m/s
# ctrl wind speed data is already in m/s
# 
# Path for laptop
# wind_path = r"S:\CHM\ExposureScienceLab\Flint Maternal Health Study\windrose\wind_data_epa\hourly_WIND_2023.csv"
# 
# Path for work computer
wind_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\wind_data_epa\hourly_WIND_2023.csv"
wind_ctrl_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\verification_data\wind_verification.csv"
# ----------------------------------------------------- #

# using this bc vpn make it slow
# tmp_pm_path = r"C:\Users\tuann\Downloads\hourly_88101_2023\hourly_88101_2023.csv"
# tmp_wind_path = r"C:\Users\tuann\Downloads\hourly_WIND_2023\hourly_WIND_2023.csv"
# tmp_wind_path = r"C:\Users\tuann\github\esl_scripts\data\wind_rose_test.csv"

cols = ['State Code','County Code',
        'State Name','County Name',
        'Site Num','Parameter Name',
        'Latitude','Longitude',
        'Date Local','Time Local',
        'Sample Measurement','Units of Measure'
        ]

# read in data
pm_data = pd.read_csv(pm_path, usecols=cols)
pm_ctrl_data = pd.read_csv(pm_ctrl_path, usecols=cols)
wind_data = pd.read_csv(wind_path, usecols=cols)
wind_ctrl_data = pd.read_csv(wind_ctrl_path, usecols=cols)

# filter data
pm_data = pm_data[(pm_data['State Code'] == 26) & (pm_data['County Code'] == 49) & (pm_data['Site Num'] == 21)]
pm_ctrl_data = pm_ctrl_data[(pm_ctrl_data['State Code'] == 26) & (pm_ctrl_data['County Code'] == 49) & (pm_ctrl_data['Site Num'] == 21)]

wind_data = wind_data[(wind_data['State Code'] == 26) & (wind_data['County Code'] == 49) & (wind_data['Site Num'] == 21)]
wind_ctrl_data = wind_ctrl_data[(wind_ctrl_data['State Code'] == 26) & (wind_ctrl_data['County Code'] == 49) & (wind_ctrl_data['Site Num'] == 21)]

wind_dir_data = wind_data[wind_data['Parameter Name'] == 'Wind Direction - Resultant']
wind_speed_data = wind_data[wind_data['Parameter Name'] == 'Wind Speed - Resultant']
wind_dir_ctrl_data = wind_ctrl_data[wind_ctrl_data['Parameter Name'] == 'Wind Direction - Resultant']
wind_speed_ctrl_data = wind_ctrl_data[wind_ctrl_data['Parameter Name'] == 'Wind Speed - Resultant']

# print(pm_data['Parameter Name'].unique()) # there was only PM2.5
# print(wind_data['Parameter Name'].unique()) # only speed and direction
# pm_dat.columns
# print(pm_dat.head())
# print(wind_data.head())
# print(wind_dir_data)
# print(wind_speed_data)

# ---------------------- PM data work ---------------------- #
pm_data['Sample Measurement'] = pd.to_numeric(pm_data['Sample Measurement'], errors='coerce')
pm_data['Sample Measurement'] = pm_data['Sample Measurement'].fillna(0)
pm_data['Sample Measurement'] = pm_data['Sample Measurement'].astype(float)

pm_data_daily = pm_data[['Date Local','Sample Measurement']]
pm_data_daily = pm_data_daily.groupby('Date Local').mean()
pm_data_daily = pm_data_daily.reset_index()
print(pm_data_daily)

pm_ctrl_data['Sample Measurement'] = pd.to_numeric(pm_ctrl_data['Sample Measurement'], errors='coerce')
pm_ctrl_data['Sample Measurement'] = pm_ctrl_data['Sample Measurement'].fillna(0)
pm_ctrl_data['Sample Measurement'] = pm_ctrl_data['Sample Measurement'].astype(float)

pm_ctrl_data_daily = pm_ctrl_data[['Date Local','Sample Measurement']]
pm_ctrl_data_daily = pm_ctrl_data_daily.groupby('Date Local').mean()
pm_ctrl_data_daily = pm_ctrl_data_daily.reset_index()
print(pm_ctrl_data_daily) # pm values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'
# ----------------------------------------------------- #

# ---------------------- Wind data work ---------------------- #
# wind_dir_data['Date Local'] = pd.to_datetime(wind_dir_data['Date Local'])
# wind_dir_data['Time Local'] = pd.to_datetime(wind_dir_data['Time Local'], format='%H:%M')
# wind_speed_data['Date Local'] = pd.to_datetime(wind_speed_data['Date Local'])
# wind_speed_data['Time Local'] = pd.to_datetime(wind_speed_data['Time Local'], format='%H:%M')

wind_dir_data_daily = wind_dir_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]
wind_speed_data_daily = wind_speed_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]
print(wind_dir_data_daily.groupby('Date Local')['Sample Measurement'].mean())
print(wind_speed_data_daily.groupby('Date Local')['Sample Measurement'].mean())

wind_dir_ctrl_data_daily = wind_dir_ctrl_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]
wind_speed_ctrl_data_daily = wind_speed_ctrl_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]

print(wind_dir_ctrl_data_daily.groupby('Date Local')['Sample Measurement'].mean()) # wind dir values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'
print(wind_speed_ctrl_data_daily.groupby('Date Local')['Sample Measurement'].mean()) # wind speed values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'
# print(wind_dir_data_daily['Time Local'])
# print(wind_dir_data_daily['Date Local'])
# print(wind_speed_data_daily['Time Local'])
# print(wind_speed_data_daily['Date Local'])

# convert knots to m/s
wind_speed_data_daily.loc[:, 'Sample Measurement'] = wind_speed_data_daily['Sample Measurement'] * 0.514444
print(wind_speed_data_daily)

def get_weighted_dir(wind_dir_df, wind_spd_df):
    df = pd.DataFrame(columns=['Date Local','weighted_velocity','weighted_direction','weighted_direction_str (blowing from)'])
    # iter_counter = 0

    for date in wind_dir_df['Date Local'].unique():
        # combine the wind direction and wind speed data for that date and time
        wind_dir = wind_dir_df[wind_dir_df['Date Local'] == date]
        # print(f"unique num of hours for dir: {len(wind_dir['Time Local'].unique())}")
        # print(f"total num of hours for dir: {len(wind_dir['Time Local'])}")
        
        wind_speed = wind_spd_df[wind_spd_df['Date Local'] == date] 
        # print(f"unique num of hours for dir: {len(wind_speed['Time Local'].unique())}")
        # print(f"total num of hours for dir: {len(wind_speed['Time Local'])}")
        
        try:
            wind_data_daily = pd.merge(wind_dir, wind_speed, on='Time Local')
            print('merge good')
        except Exception as e:
            print(e)
            break

        # drop unnecessary columns
        wind_data_daily = wind_data_daily.drop(columns=['Date Local_y'])
        # len(wind_data_daily)
        random_indexes = np.random.randint(0, 23, 3)
        print(f"random indexes to be checked: {random_indexes}")
        
        # print(wind_data_daily)

        try:
            for i in random_indexes:
                if i > (len(wind_data_daily) - 1):
                    i = len(wind_data_daily) - 1
                print(f"index being checked: {i}")
                wind_data_daily_row = wind_data_daily.loc[i]
                # print(f"wind_data_daily row {i}\n{wind_data_daily_row}")
                date_to_check = wind_data_daily_row['Date Local_x']
                time_to_check = wind_data_daily_row['Time Local']
                wind_dir_to_check = float(wind_data_daily_row['Sample Measurement_x'])
                wind_speed_to_check = wind_data_daily_row['Sample Measurement_y']
                direction_in_raw_data = float(wind_dir_df[(wind_dir_df['Date Local'] == date_to_check) & (wind_dir_df['Time Local'] == time_to_check)]['Sample Measurement'].iloc[0])
                speed_in_raw_data = float(wind_spd_df[(wind_spd_df['Date Local'] == date_to_check) & (wind_spd_df['Time Local'] == time_to_check)]['Sample Measurement'].iloc[0])
                
                if direction_in_raw_data == wind_dir_to_check:
                    print('Wind direction is correct')
                    # print(f"""Date: {date_to_check}, Time: {time_to_check}\nWind speed in raw data: {direction_in_raw_data}\nWind speed in processed data: {wind_dir_to_check}""")
                else:
                    print('Wind direction is incorrect')
                    print(f"""Date: {date_to_check}, Time: {time_to_check}\nWind speed in raw data: {direction_in_raw_data}\nWind speed in processed data: {wind_dir_to_check}""")
                    break
                if speed_in_raw_data == wind_speed_to_check:
                    print('Wind speed is correct')
                    # print(f"""Date: {date_to_check}, Time: {time_to_check}\nWind speed in raw data: {speed_in_raw_data}\nWind speed in processed data: {wind_speed_to_check}""")
                    
                else:
                    print('Wind speed is incorrect')
                    print(f"""Date: {date_to_check}, Time: {time_to_check}\nWind speed in raw data: {speed_in_raw_data}\nWind speed in processed data: {wind_speed_to_check}""")
                    break
        except Exception as e:
            print(e)

        ########################### weighted velocity is coming out right ########################################    
        print(f"Now performing calculations for {date}...")
        wind_data_daily['x_component'] = wind_data_daily['Sample Measurement_y'] * np.cos(2 * np.pi * (90 - wind_data_daily['Sample Measurement_x']) / 360)
        wind_data_daily['y_component'] = wind_data_daily['Sample Measurement_y'] * np.sin(2 * np.pi * (90 - wind_data_daily['Sample Measurement_x']) / 360)
        
        mean_x_component = wind_data_daily['x_component'].mean()
        print(f"Mean x component: {mean_x_component}")
        mean_y_component = wind_data_daily['y_component'].mean()
        print(f"Mean y component: {mean_y_component}")
        
        weighted_velocity = np.sqrt(mean_x_component**2 + mean_y_component**2)
        print(f"Weighted velocity for {date}: {weighted_velocity}")
        ##########################################################################################################

        ########################### weighted velocity is coming out right ########################################    
        weighted_direction = PolarCoord(mean_x_component, mean_y_component)
        print(f"weighted direction: {weighted_direction}")
        weighted_direction_str = degToCompass(weighted_direction)
        print(f"weighted direction str: {weighted_direction_str}")
        ##########################################################################################################

        row = pd.Series({
            'Date Local': date,
            'weighted_velocity': weighted_velocity,
            'weighted_direction': weighted_direction,
            'weighted_direction_str (blowing from)': weighted_direction_str
        })
        tmp = pd.DataFrame([row], columns=['Date Local','weighted_velocity','weighted_direction','weighted_direction_str (blowing from)'])
        df = pd.concat([df, tmp], ignore_index=True)

        print(f"num of unique weighted directions: {len(df['weighted_direction_str (blowing from)'].unique())}")

        # iter_counter += 1
        # if iter_counter < 30:
        #     continue
        # else:
        #     break
    return df

def create_windrose(weighted_df, pm_df, output_dir, path_to_output_xlsx):
    print(len(weighted_df['Date Local'].unique()))
    print(len(pm_df['Date Local'].unique()))
    try:
        df = pd.merge(weighted_df, pm_df, on='Date Local')
        print('merge good')
        print(df)
    except Exception as e:
        print(e)

    plot_data_df = pd.DataFrame()
    
    print(f"num of directions in data: {len(df['weighted_direction_str (blowing from)'].unique())}")

    for direction in df['weighted_direction_str (blowing from)'].unique():
        print(direction)
        print(df[df['weighted_direction_str (blowing from)'] == direction]['Sample Measurement'].mean())

        # add the mean for direction to df
        x = direction_to_radians(direction)
        print(x)
        row = pd.Series({
            'Direction': direction,
            'Direction (Radians)': x,
            'Mean PM2.5': df[df['weighted_direction_str (blowing from)'] == direction]['Sample Measurement'].mean()
        })

        row_df = pd.DataFrame([row], columns=['Direction','Direction (Radians)','Mean PM2.5'])
        plot_data_df = pd.concat([plot_data_df, row_df], ignore_index=True)
    
    order = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    plot_data_df.set_index('Direction', inplace=True)
    plot_data_df = plot_data_df.reindex(order)
    plot_data_df.reset_index(inplace=True)
    plot_data_df = pd.concat([plot_data_df, plot_data_df.iloc[[0]]])
    print(plot_data_df)

    # # create windrose with each direction and avg pm2.5 for that direction
    direction = plot_data_df['Direction (Radians)']
    pm = plot_data_df['Mean PM2.5']

    fig, ax = plt.subplots(1, 2, figsize=(10, 6), subplot_kw={'projection': 'polar'})
    ax[0].plot(direction, pm)

    tmp = plot_data_df[['Direction', 'Mean PM2.5']].copy()
    tmp['Mean PM2.5'] = tmp['Mean PM2.5'].round(4)
    table_data = tmp.values.tolist()
    table_data.insert(0, list(tmp.columns))
    ax[1].axis('tight')
    ax[1].axis('off')
    ax[1].table(cellText=table_data, cellLoc='center', loc='center')

    # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    # ax.plot(direction, pm) # theta, radius
    # ax.set_xticks(np.linspace(0, 2 * np.pi, 16, endpoint=False))
    # ax.set_xticklabels(order)
    # ax.set_rmax(max(pm)+max(pm)*0.25) # set radius max to 25% above the max pm val for now 
    # ax.grid(True)
    # ax.set_theta_zero_location('N')
    # ax.set_theta_direction(-1)
    # ax.set_rlabel_position(0)

    ax[0].plot(direction, pm) # theta, radius
    ax[0].set_xticks(np.linspace(0, 2 * np.pi, 16, endpoint=False))
    ax[0].set_xticklabels(order)
    ax[0].set_rmax(max(pm)+max(pm)*0.25) # set radius max to 25% above the max pm val for now 
    ax[0].grid(True)
    ax[0].set_theta_zero_location('N')
    ax[0].set_theta_direction(-1)
    ax[0].set_rlabel_position(0)

    plt.title('Windrose for Flint, Michigan')
    fig_output = os.path.join(output_dir, 'wind_rose.png')
    plt.savefig(fig_output)

    # # export dfs to the sheet
    with pd.ExcelWriter(path_to_output_xlsx) as writer:
        pm_df.to_excel(writer, sheet_name='PM Data')
        weighted_df.to_excel(writer, sheet_name='Weighted Calculations')
        plot_data_df.to_excel(writer, sheet_name='Final')
    return None

weighted_df = get_weighted_dir(wind_dir_data_daily, wind_speed_data_daily)
# weighted_df = get_weighted_dir(wind_dir_ctrl_data_daily, wind_speed_ctrl_data_daily)
# print(weighted_df)

output_dir = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\output"
export_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\export\flint_windrose.xlsx"        
aaa = create_windrose(weighted_df, pm_data_daily, output_dir, export_path)
# tmp = create_windrose(weighted_df, pm_ctrl_data_daily)