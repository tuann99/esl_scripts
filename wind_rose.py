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

def combine_df_wind_and_pm(weighted_df, pm_df):
    plot_data_df = pd.DataFrame()
    
    try:
        df = pd.merge(weighted_df, pm_df, on='Date Local')
        print('merge good')
    except Exception as e:
        print(e)

    for direction in df['weighted_direction_str (blowing from)'].unique():
        x = direction_to_radians(direction)
        row = pd.Series({
            'Direction': direction,
            'Direction (Radians)': x,
            'Mean PM2.5': df[df['weighted_direction_str (blowing from)'] == direction]['Sample Measurement'].mean().round(4)
        })

        row_df = pd.DataFrame([row], columns=['Direction','Direction (Radians)','Mean PM2.5'])
        plot_data_df = pd.concat([plot_data_df, row_df], ignore_index=True)
    return plot_data_df
    
def create_combined_dataframe(plot_data_df, plot_data_df_2=None, plot_data_df_3=None, plot_data_df_4=None):
    if plot_data_df_2 is None and plot_data_df_3 is None and plot_data_df_4 is None:
        plot_data_df.rename(columns={'Mean PM2.5': '2020 PM2.5 (ug/m3)'}, inplace=True)
        combined_df = plot_data_df
        return combined_df
    elif plot_data_df_2 and plot_data_df_3 is None:
        plot_data_df.rename(columns={'Mean PM2.5': '2023 PM2.5 (ug/m3)'}, inplace=True)
        plot_data_df_2.rename(columns={'Mean PM2.5': '2022 PM2.5 (ug/m3)'}, inplace=True)
        combined_df = pd.merge(plot_data_df, plot_data_df_2, on=['Direction', 'Direction (Radians)'])
        return combined_df
    elif plot_data_df_4 is None:
        plot_data_df.rename(columns={'Mean PM2.5': '2020 PM2.5 (ug/m3)'}, inplace=True)
        plot_data_df_2.rename(columns={'Mean PM2.5': '2021 PM2.5 (ug/m3)'}, inplace=True)
        plot_data_df_3.rename(columns={'Mean PM2.5': '2022 PM2.5 (ug/m3)'}, inplace=True)
        combined_df = pd.merge(plot_data_df, plot_data_df_2, on=['Direction', 'Direction (Radians)'])
        combined_df = pd.merge(combined_df, plot_data_df_3, on=['Direction', 'Direction (Radians)'])
        return combined_df
    else:
        plot_data_df.rename(columns={'Mean PM2.5': '2020 PM2.5 (ug/m3)'}, inplace=True)
        plot_data_df_2.rename(columns={'Mean PM2.5': '2021 PM2.5 (ug/m3)'}, inplace=True)
        plot_data_df_3.rename(columns={'Mean PM2.5': '2022 PM2.5 (ug/m3)'}, inplace=True)
        plot_data_df_4.rename(columns={'Mean PM2.5': '2023 PM2.5 (ug/m3)'}, inplace=True)
        combined_df = pd.merge(plot_data_df, plot_data_df_2, on=['Direction', 'Direction (Radians)'])
        combined_df = pd.merge(combined_df, plot_data_df_3, on=['Direction', 'Direction (Radians)'])
        combined_df = pd.merge(combined_df, plot_data_df_4, on=['Direction', 'Direction (Radians)'])
        return combined_df

def format_combined_df(combined_df):
    try:
        order = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        formatted_df = combined_df.copy()
        formatted_df.set_index('Direction', inplace=True)
        formatted_df = formatted_df.reindex(order)
        formatted_df.reset_index(inplace=True)
        formatted_df = pd.concat([formatted_df, formatted_df.iloc[[0]]])
        return formatted_df
    except Exception as e:
        print(e)
        return None

def create_windrose(df1, df2=None):
    """
    Description: Create a windrose plot

    Input: df1 (pd.DataFrame) - the first dataframe to be plotted
           df2 (pd.DataFrame) - the second dataframe to be plotted
    Output: None
    """
    if df2 is not None:
        combined_df = create_combined_dataframe(df1, df2)
    else:
        combined_df = df1

    formatted_df = format_combined_df(combined_df)

    direction = formatted_df['Direction (Radians)']
    pm_2022 = formatted_df['2022 PM2.5 (ug/m3)']
    pm_2023 = formatted_df.get('2023 PM2.5 (ug/m3)', None)

    fig, ax = plt.subplots(1, 2 if pm_2023 is not None else 1, figsize=(14, 6), subplot_kw={'projection': 'polar'})
    ax[0].plot(direction, pm_2022, color='red')
    if pm_2023 is not None:
        ax[0].plot(direction, pm_2023, color='blue')
    

    direction = combined_df['Direction (Radians)']
    pm_2022 = combined_df['2022 PM2.5 (ug/m3)']
    pm_2023 = combined_df['2023 PM2.5 (ug/m3)']

    # fig, ax = plt.subplots(1, 3, figsize=(16, 6), subplot_kw={'projection': 'polar'})
    fig, ax = plt.subplots(1, 2, figsize=(14, 6), subplot_kw={'projection': 'polar'})
    ax[0].plot(direction, pm_2022, color='red')
    ax[0].plot(direction, pm_2023, color='blue')

    selected_columns_df = combined_df[['Direction', '2022 PM2.5 (ug/m3)', '2023 PM2.5 (ug/m3)']]
    selected_columns_df = selected_columns_df.drop(selected_columns_df.index[-1])
    header_lengths = [len(header) for header in selected_columns_df.columns.values.tolist()]
    total_length = sum(header_lengths)
    col_widths = [length / total_length for length in header_lengths]
    table_data = [selected_columns_df.columns.values.tolist()] + selected_columns_df.values.tolist()
    ax[1].axis('tight')
    ax[1].axis('off')
    table = ax[1].table(cellText=table_data, colWidths=col_widths, loc='best', cellLoc='right')
    
    # tmp = plot_data_df[['Direction', 'Mean PM2.5']].copy()
    # tmp['Mean PM2.5'] = tmp['Mean PM2.5'].round(4)
    # table_data = tmp.values.tolist()
    # table_data.insert(0, list(tmp.columns))
    # ax[1].axis('tight')
    # ax[1].axis('off')
    # ax[1].table(cellText=table_data, cellLoc='center', loc='center')
    # ax[1].title.set_text('2023')

    # tmp_2 = plot_data_df_2[['Direction', 'Mean PM2.5']].copy()
    # tmp_2['Mean PM2.5'] = tmp_2['Mean PM2.5'].round(4)
    # table_data_2 = tmp_2.values.tolist()
    # table_data_2.insert(0, list(tmp_2.columns))
    # ax[2].axis('tight')
    # ax[2].axis('off')
    # ax[2].table(cellText=table_data_2, cellLoc='center', loc='center')
    # ax[2].title.set_text('2022')

    # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    # ax.plot(direction, pm) # theta, radius
    # ax.set_xticks(np.linspace(0, 2 * np.pi, 16, endpoint=False))
    # ax.set_xticklabels(order)
    # ax.set_rmax(max(pm)+max(pm)*0.25) # set radius max to 25% above the max pm val for now 
    # ax.grid(True)
    # ax.set_theta_zero_location('N')
    # ax.set_theta_direction(-1)
    # ax.set_rlabel_position(0)
    
    # ax[0].plot(direction, pm_2023) # theta, radius
    ax[0].set_xticks(np.linspace(0, 2 * np.pi, 16, endpoint=False))
    ax[0].set_xticklabels(order)
    if max(pm_2023) > max(pm_2022):
        ax[0].set_rmax(max(pm_2023)+max(pm_2023)*0.25)
    else:
        ax[0].set_rmax(max(pm_2022)+max(pm_2022)*0.25)
    
    # ax[0].set_rmax(max(pm)+max(pm)*0.25) # set radius max to 25% above the max pm val for now 
    ax[0].grid(True)
    ax[0].set_theta_zero_location('N')
    ax[0].set_theta_direction(-1)
    ax[0].set_rlabel_position(0)
    ax[0].legend([2022, 2023], loc='upper left', bbox_to_anchor=(1, 1))
    
    # plt.title('Windrose for Flint, Michigan', loc='center', pad=10)
    fig.suptitle('Windrose for Flint, Michigan', fontsize=16)
    plt.show()
    return None

def create_transparent_windrose(weighted_df, pm_df, weighted_df_2=None, pm_df_2=None, weighted_df_3=None, pm_df_3=None, weighted_df_4=None, pm_df_4=None):
    
    # if other years are not provided, just plot the first year
    if weighted_df_2 is None:
        df = pd.merge(weighted_df, pm_df, on='Date Local')
        plot_data_df = pd.DataFrame()
        for direction in df['weighted_direction_str (blowing from)'].unique():
            x = direction_to_radians(direction)
            row = pd.Series({
                'Direction': direction,
                'Direction (Radians)': x,
                'Mean PM2.5': df[df['weighted_direction_str (blowing from)'] == direction]['Sample Measurement'].mean().round(4)
            })

            row_df = pd.DataFrame([row], columns=['Direction','Direction (Radians)','Mean PM2.5'])
            plot_data_df = pd.concat([plot_data_df, row_df], ignore_index=True)
        print(f"just passed the direction for loop here is the df \n{plot_data_df}")
        print(f"here is the type of 'plot_data_df' {type(plot_data_df)}")
        combined_df = create_combined_dataframe(plot_data_df)
        order = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        combined_df.set_index('Direction', inplace=True)
        combined_df = combined_df.reindex(order)
        combined_df.reset_index(inplace=True)
        combined_df = pd.concat([combined_df, combined_df.iloc[[0]]])
        direction = combined_df['Direction (Radians)']
        pm_2020 = combined_df['2020 PM2.5 (ug/m3)']
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(direction, pm_2020, color='red')
        ax.set_xticks(np.linspace(0, 2 * np.pi, 16, endpoint=False))
        ax.set_xticklabels(order)
        ax.set_rmax(max(pm_2020)+max(pm_2020)*0.1)
        ax.grid(True)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_rlabel_position(0)
        
        plt.savefig(r'S:\ExposureScienceLab\Flint Maternal Health Study\windrose\output\transparent_windrose_2.png', transparent=True)
        plt.show()
        return None
    else:
        try:
            df = pd.merge(weighted_df, pm_df, on='Date Local')
            df_2 = pd.merge(weighted_df_2, pm_df_2, on='Date Local')
            df_3 = pd.merge(weighted_df_3, pm_df_3, on='Date Local')
            df_4 = pd.merge(weighted_df_4, pm_df_4, on='Date Local')
            print('merge good')
        except Exception as e:
            print(e)

        plot_data_df = pd.DataFrame()
        plot_data_df_2 = pd.DataFrame()
        plot_data_df_3 = pd.DataFrame()
        plot_data_df_4 = pd.DataFrame()
        
        for direction in df['weighted_direction_str (blowing from)'].unique():
            x = direction_to_radians(direction)
            row = pd.Series({
                'Direction': direction,
                'Direction (Radians)': x,
                'Mean PM2.5': df[df['weighted_direction_str (blowing from)'] == direction]['Sample Measurement'].mean().round(4)
            })

            row_df = pd.DataFrame([row], columns=['Direction','Direction (Radians)','Mean PM2.5'])
            plot_data_df = pd.concat([plot_data_df, row_df], ignore_index=True)

        for direction in df_2['weighted_direction_str (blowing from)'].unique():
            x = direction_to_radians(direction)
            row = pd.Series({
                'Direction': direction,
                'Direction (Radians)': x,
                'Mean PM2.5': df_2[df_2['weighted_direction_str (blowing from)'] == direction]['Sample Measurement'].mean().round(4)
            })

            row_df = pd.DataFrame([row], columns=['Direction','Direction (Radians)','Mean PM2.5'])
            plot_data_df_2 = pd.concat([plot_data_df_2, row_df], ignore_index=True)
        
        for direction in df_3['weighted_direction_str (blowing from)'].unique():
            x = direction_to_radians(direction)
            row = pd.Series({
                'Direction': direction,
                'Direction (Radians)': x,
                'Mean PM2.5': df_3[df_3['weighted_direction_str (blowing from)'] == direction]['Sample Measurement'].mean().round(4)
            })

            row_df = pd.DataFrame([row], columns=['Direction','Direction (Radians)','Mean PM2.5'])
            plot_data_df_3 = pd.concat([plot_data_df_3, row_df], ignore_index=True)

        for direction in df_4['weighted_direction_str (blowing from)'].unique():
            x = direction_to_radians(direction)
            row = pd.Series({
                'Direction': direction,
                'Direction (Radians)': x,
                'Mean PM2.5': df_4[df_4['weighted_direction_str (blowing from)'] == direction]['Sample Measurement'].mean().round(4)
            })

            row_df = pd.DataFrame([row], columns=['Direction','Direction (Radians)','Mean PM2.5'])
            plot_data_df_4 = pd.concat([plot_data_df_4, row_df], ignore_index=True)
        
        combined_df = create_combined_dataframe(plot_data_df, plot_data_df_2, plot_data_df_3, plot_data_df_4)

        order = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        combined_df.set_index('Direction', inplace=True)
        combined_df = combined_df.reindex(order)
        combined_df.reset_index(inplace=True)
        combined_df = pd.concat([combined_df, combined_df.iloc[[0]]])

        direction = combined_df['Direction (Radians)']
        pm_2020 = combined_df['2020 PM2.5 (ug/m3)']
        pm_2021 = combined_df['2021 PM2.5 (ug/m3)']
        pm_2022 = combined_df['2022 PM2.5 (ug/m3)']
        pm_2023 = combined_df['2023 PM2.5 (ug/m3)']

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(direction, pm_2020, color='red')
        ax.plot(direction, pm_2021, color='green')
        ax.plot(direction, pm_2022, color='orange')
        ax.plot(direction, pm_2023, color='blue')
        ax.set_xticks(np.linspace(0, 2 * np.pi, 16, endpoint=False))
        ax.set_xticklabels(order)
        if max(pm_2023) > max(pm_2022):
            ax.set_rmax(max(pm_2023)+max(pm_2023)*0.25)
        else:
            ax.set_rmax(max(pm_2022)+max(pm_2022)*0.25)
        
        ax.grid(True, color='black')
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_rlabel_position(0)
        ax.legend([2020, 2021, 2022, 2023], loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.savefig(r'S:\ExposureScienceLab\Flint Maternal Health Study\windrose\output\transparent_windrose_2.png', transparent=True)
        plt.show()
        
        return None
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
pm_2022_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\pm_data_epa\hourly_88101_2022.csv"
pm_2021_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\hourly_88101_2021\hourly_88101_2021.csv"
pm_2020_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\hourly_88101_2020\hourly_88101_2020.csv"

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
wind_2022_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\hourly_WIND_2022\hourly_WIND_2022.csv"
wind_2021_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\hourly_WIND_2021\hourly_WIND_2021.csv"
wind_2020_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\hourly_WIND_2020\hourly_WIND_2020.csv"

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
pm_2022_data = pd.read_csv(pm_2022_path, usecols=cols)
pm_2021_data = pd.read_csv(pm_2021_path, usecols=cols)
pm_2020_data = pd.read_csv(pm_2020_path, usecols=cols)

wind_data = pd.read_csv(wind_path, usecols=cols)
wind_ctrl_data = pd.read_csv(wind_ctrl_path, usecols=cols)
wind_2022_data = pd.read_csv(wind_2022_path, usecols=cols)
wind_2021_data = pd.read_csv(wind_2021_path, usecols=cols)
wind_2020_data = pd.read_csv(wind_2020_path, usecols=cols)

# filter data
pm_data = pm_data[(pm_data['State Code'] == 26) & (pm_data['County Code'] == 49) & (pm_data['Site Num'] == 21)]
pm_ctrl_data = pm_ctrl_data[(pm_ctrl_data['State Code'] == 26) & (pm_ctrl_data['County Code'] == 49) & (pm_ctrl_data['Site Num'] == 21)]
pm_2022_data = pm_2022_data[(pm_2022_data['State Code'] == 26) & (pm_2022_data['County Code'] == 49) & (pm_2022_data['Site Num'] == 21)]
pm_2021_data = pm_2021_data[(pm_2021_data['State Code'] == 26) & (pm_2021_data['County Code'] == 49) & (pm_2021_data['Site Num'] == 21)]
pm_2020_data = pm_2020_data[(pm_2020_data['State Code'] == 26) & (pm_2020_data['County Code'] == 49) & (pm_2020_data['Site Num'] == 21)]

wind_data = wind_data[(wind_data['State Code'] == 26) & (wind_data['County Code'] == 49) & (wind_data['Site Num'] == 21)]
wind_ctrl_data = wind_ctrl_data[(wind_ctrl_data['State Code'] == 26) & (wind_ctrl_data['County Code'] == 49) & (wind_ctrl_data['Site Num'] == 21)]
wind_2022_data = wind_2022_data[(wind_2022_data['State Code'] == 26) & (wind_2022_data['County Code'] == 49) & (wind_2022_data['Site Num'] == 21)]
wind_2021_data = wind_2021_data[(wind_2021_data['State Code'] == 26) & (wind_2021_data['County Code'] == 49) & (wind_2021_data['Site Num'] == 21)]
wind_2020_data = wind_2020_data[(wind_2020_data['State Code'] == 26) & (wind_2020_data['County Code'] == 49) & (wind_2020_data['Site Num'] == 21)]

wind_dir_data = wind_data[wind_data['Parameter Name'] == 'Wind Direction - Resultant']
wind_speed_data = wind_data[wind_data['Parameter Name'] == 'Wind Speed - Resultant']

wind_dir_ctrl_data = wind_ctrl_data[wind_ctrl_data['Parameter Name'] == 'Wind Direction - Resultant']
wind_speed_ctrl_data = wind_ctrl_data[wind_ctrl_data['Parameter Name'] == 'Wind Speed - Resultant']

wind_dir_2022_data = wind_2022_data[wind_2022_data['Parameter Name'] == 'Wind Direction - Resultant']
wind_speed_2022_data = wind_2022_data[wind_2022_data['Parameter Name'] == 'Wind Speed - Resultant']

wind_dir_2021_data = wind_2021_data[wind_2021_data['Parameter Name'] == 'Wind Direction - Resultant']
wind_speed_2021_data = wind_2021_data[wind_2021_data['Parameter Name'] == 'Wind Speed - Resultant']

wind_dir_2020_data = wind_2020_data[wind_2020_data['Parameter Name'] == 'Wind Direction - Resultant']
wind_speed_2020_data = wind_2020_data[wind_2020_data['Parameter Name'] == 'Wind Speed - Resultant']
print(wind_dir_2020_data)
print(wind_speed_2020_data)

# print(pm_data['Parameter Name'].unique()) # there was only PM2.5
# print(wind_data['Parameter Name'].unique()) # only speed and direction
# pm_dat.columns
# print(pm_dat.head())
# print(wind_data.head())
# print(wind_dir_data)
# print(wind_speed_data)

# get latitudes and longitudes for site 21
latitude_2023 = pm_data['Latitude'].iloc[0]
longitude_2023 = pm_data['Longitude'].iloc[0]

# just checking if its the same still
# latitude_2022 = pm_2022_data['Latitude'].iloc[0]
# longitude_2022 = pm_2022_data['Longitude'].iloc[0]

# print(f"Latitude 2023: {latitude_2023}, Longitude 2023: {longitude_2023}")
# print(f"Latitude 2022: {latitude_2022}, Longitude 2022: {longitude_2022}")

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

pm_2022_data['Sample Measurement'] = pd.to_numeric(pm_2022_data['Sample Measurement'], errors='coerce')
pm_2022_data['Sample Measurement'] = pm_2022_data['Sample Measurement'].fillna(0)
pm_2022_data['Sample Measurement'] = pm_2022_data['Sample Measurement'].astype(float)

pm_2022_data_daily = pm_2022_data[['Date Local','Sample Measurement']]
pm_2022_data_daily = pm_2022_data_daily.groupby('Date Local').mean()
pm_2022_data_daily = pm_2022_data_daily.reset_index()
print(pm_2022_data_daily) # pm values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'

pm_2021_data['Sample Measurement'] = pd.to_numeric(pm_2021_data['Sample Measurement'], errors='coerce')
pm_2021_data['Sample Measurement'] = pm_2021_data['Sample Measurement'].fillna(0)
pm_2021_data['Sample Measurement'] = pm_2021_data['Sample Measurement'].astype(float)

pm_2021_data_daily = pm_2021_data[['Date Local','Sample Measurement']]
pm_2021_data_daily = pm_2021_data_daily.groupby('Date Local').mean()
pm_2021_data_daily = pm_2021_data_daily.reset_index()
print(pm_2021_data_daily) # pm values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'

pm_2020_data['Sample Measurement'] = pd.to_numeric(pm_2020_data['Sample Measurement'], errors='coerce')
pm_2020_data['Sample Measurement'] = pm_2020_data['Sample Measurement'].fillna(0)
pm_2020_data['Sample Measurement'] = pm_2020_data['Sample Measurement'].astype(float)

pm_2020_data_daily = pm_2020_data[['Date Local','Sample Measurement']]
pm_2020_data_daily = pm_2020_data_daily.groupby('Date Local').mean()
pm_2020_data_daily = pm_2020_data_daily.reset_index()
print(pm_2020_data_daily) # pm values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'
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

wind_dir_2022_data_daily = wind_dir_2022_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]
wind_speed_2022_data_daily = wind_speed_2022_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]
# wind_dir_2022_data_daily = wind_dir_2022_data_daily.groupby('Date Local')['Sample Measurement'].mean()
# wind_speed_2022_data_daily = wind_speed_2022_data_daily.groupby('Date Local')['Sample Measurement'].mean()
print(wind_dir_2022_data_daily) # wind dir values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'
print(wind_speed_2022_data_daily) # wind speed values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'

wind_dir_2021_data_daily = wind_dir_2021_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]
wind_speed_2021_data_daily = wind_speed_2021_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]
# wind_dir_2021_data_daily = wind_dir_2021_data_daily.groupby('Date Local')['Sample Measurement'].mean()
# wind_speed_2021_data_daily = wind_speed_2021_data_daily.groupby('Date Local')['Sample Measurement'].mean()
print(wind_dir_2021_data_daily.groupby('Date Local')['Sample Measurement'].mean()) # wind dir values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'
print(wind_speed_2021_data_daily.groupby('Date Local')['Sample Measurement'].mean()) # wind speed values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'

wind_dir_2020_data_daily = wind_dir_2020_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]
wind_speed_2020_data_daily = wind_speed_2020_data[['Date Local','Sample Measurement','Parameter Name', 'Time Local']]
# wind_dir_2020_data_daily = wind_dir_2020_data_daily.groupby('Date Local')['Sample Measurement'].mean()
# wind_speed_2020_data_daily = wind_speed_2020_data_daily.groupby('Date Local')['Sample Measurement'].mean()
print(wind_dir_2020_data_daily.groupby('Date Local')['Sample Measurement'].mean()) # wind dir values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'
print(wind_speed_2020_data_daily.groupby('Date Local')['Sample Measurement'].mean()) # wind speed values check out with data in 'wind_direction_weighted_ambient_combined.xlsm'

# print(wind_dir_data_daily['Time Local'])
# print(wind_dir_data_daily['Date Local'])
# print(wind_speed_data_daily['Time Local'])
# print(wind_speed_data_daily['Date Local'])

# convert knots to m/s
wind_speed_data_daily.loc[:, 'Sample Measurement'] = wind_speed_data_daily['Sample Measurement'] * 0.514444
print(wind_speed_data_daily)

wind_speed_2022_data_daily.loc[:, 'Sample Measurement'] = wind_speed_2022_data_daily['Sample Measurement'] * 0.514444
print(wind_speed_2022_data_daily)

wind_speed_2021_data_daily.loc[:, 'Sample Measurement'] = wind_speed_2021_data_daily['Sample Measurement'] * 0.514444
print(wind_speed_2021_data_daily)

wind_speed_2020_data_daily.loc[:, 'Sample Measurement'] = wind_speed_2020_data_daily['Sample Measurement'] * 0.514444
print(wind_speed_2020_data_daily)

def create_windrose(weighted_df, pm_df, weighted_df_2, pm_df_2, output_dir, path_to_output_xlsx):
    print(len(weighted_df['Date Local'].unique()))
    print(len(pm_df['Date Local'].unique()))
    try:
        df = pd.merge(weighted_df, pm_df, on='Date Local')
        df_2 = pd.merge(weighted_df_2, pm_df_2, on='Date Local')
        print('merge good')
        print(df)
        print(df_2)
    except Exception as e:
        print(e)

    plot_data_df = pd.DataFrame()
    plot_data_df_2 = pd.DataFrame()
    
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
            'Mean PM2.5': df[df['weighted_direction_str (blowing from)'] == direction]['Sample Measurement'].mean().round(4)
        })

        row_df = pd.DataFrame([row], columns=['Direction','Direction (Radians)','Mean PM2.5'])
        plot_data_df = pd.concat([plot_data_df, row_df], ignore_index=True)

    for direction in df_2['weighted_direction_str (blowing from)'].unique():
        print(direction)
        print(df_2[df_2['weighted_direction_str (blowing from)'] == direction]['Sample Measurement'].mean())

        # add the mean for direction to df
        x = direction_to_radians(direction)
        print(x)
        row = pd.Series({
            'Direction': direction,
            'Direction (Radians)': x,
            'Mean PM2.5': df_2[df_2['weighted_direction_str (blowing from)'] == direction]['Sample Measurement'].mean().round(4)
        })

        row_df = pd.DataFrame([row], columns=['Direction','Direction (Radians)','Mean PM2.5'])
        plot_data_df_2 = pd.concat([plot_data_df_2, row_df], ignore_index=True)
    
    combined_df = create_combined_dataframe(plot_data_df_2, plot_data_df)
    print(combined_df)

    order = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    combined_df.set_index('Direction', inplace=True)
    combined_df = combined_df.reindex(order)
    combined_df.reset_index(inplace=True)
    combined_df = pd.concat([combined_df, combined_df.iloc[[0]]])
    print(combined_df)

    # plot_data_df.set_index('Direction', inplace=True)
    # plot_data_df = plot_data_df.reindex(order)
    # plot_data_df.reset_index(inplace=True)
    # plot_data_df = pd.concat([plot_data_df, plot_data_df.iloc[[0]]])
    # print(plot_data_df)

    # plot_data_df_2.set_index('Direction', inplace=True)
    # plot_data_df_2 = plot_data_df_2.reindex(order)
    # plot_data_df_2.reset_index(inplace=True)
    # plot_data_df_2 = pd.concat([plot_data_df_2, plot_data_df_2.iloc[[0]]])
    # print(plot_data_df_2)

    # # create windrose with each direction and avg pm2.5 for that direction
    # direction = plot_data_df['Direction (Radians)']
    direction = combined_df['Direction (Radians)']
    pm_2022 = combined_df['2022 PM2.5 (ug/m3)']
    pm_2023 = combined_df['2023 PM2.5 (ug/m3)']

    # fig, ax = plt.subplots(1, 3, figsize=(16, 6), subplot_kw={'projection': 'polar'})
    fig, ax = plt.subplots(1, 2, figsize=(14, 6), subplot_kw={'projection': 'polar'})
    ax[0].plot(direction, pm_2022, color='red')
    ax[0].plot(direction, pm_2023, color='blue')

    selected_columns_df = combined_df[['Direction', '2022 PM2.5 (ug/m3)', '2023 PM2.5 (ug/m3)']]
    selected_columns_df = selected_columns_df.drop(selected_columns_df.index[-1])
    header_lengths = [len(header) for header in selected_columns_df.columns.values.tolist()]
    total_length = sum(header_lengths)
    col_widths = [length / total_length for length in header_lengths]
    table_data = [selected_columns_df.columns.values.tolist()] + selected_columns_df.values.tolist()
    ax[1].axis('tight')
    ax[1].axis('off')
    table = ax[1].table(cellText=table_data, colWidths=col_widths, loc='best', cellLoc='right')
    
    # tmp = plot_data_df[['Direction', 'Mean PM2.5']].copy()
    # tmp['Mean PM2.5'] = tmp['Mean PM2.5'].round(4)
    # table_data = tmp.values.tolist()
    # table_data.insert(0, list(tmp.columns))
    # ax[1].axis('tight')
    # ax[1].axis('off')
    # ax[1].table(cellText=table_data, cellLoc='center', loc='center')
    # ax[1].title.set_text('2023')

    # tmp_2 = plot_data_df_2[['Direction', 'Mean PM2.5']].copy()
    # tmp_2['Mean PM2.5'] = tmp_2['Mean PM2.5'].round(4)
    # table_data_2 = tmp_2.values.tolist()
    # table_data_2.insert(0, list(tmp_2.columns))
    # ax[2].axis('tight')
    # ax[2].axis('off')
    # ax[2].table(cellText=table_data_2, cellLoc='center', loc='center')
    # ax[2].title.set_text('2022')

    # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    # ax.plot(direction, pm) # theta, radius
    # ax.set_xticks(np.linspace(0, 2 * np.pi, 16, endpoint=False))
    # ax.set_xticklabels(order)
    # ax.set_rmax(max(pm)+max(pm)*0.25) # set radius max to 25% above the max pm val for now 
    # ax.grid(True)
    # ax.set_theta_zero_location('N')
    # ax.set_theta_direction(-1)
    # ax.set_rlabel_position(0)
    
    # ax[0].plot(direction, pm_2023) # theta, radius
    ax[0].set_xticks(np.linspace(0, 2 * np.pi, 16, endpoint=False))
    ax[0].set_xticklabels(order)
    if max(pm_2023) > max(pm_2022):
        ax[0].set_rmax(max(pm_2023)+max(pm_2023)*0.25)
    else:
        ax[0].set_rmax(max(pm_2022)+max(pm_2022)*0.25)
    
    # ax[0].set_rmax(max(pm)+max(pm)*0.25) # set radius max to 25% above the max pm val for now 
    ax[0].grid(True)
    ax[0].set_theta_zero_location('N')
    ax[0].set_theta_direction(-1)
    ax[0].set_rlabel_position(0)
    ax[0].legend([2022, 2023], loc='upper left', bbox_to_anchor=(1, 1))
    
    # plt.title('Windrose for Flint, Michigan', loc='center', pad=10)
    fig.suptitle('Windrose for Flint, Michigan', fontsize=16)
    plt.show()
    
    # fig_output = os.path.join(output_dir, 'wind_rose_2.png')
    # plt.savefig(fig_output)

    # # export dfs to the sheet
    # with pd.ExcelWriter(path_to_output_xlsx) as writer:
    #    pm_df.to_excel(writer, sheet_name='PM Data')
    #    weighted_df.to_excel(writer, sheet_name='Weighted Calculations')
    #    plot_data_df.to_excel(writer, sheet_name='Final')
    return None

weighted_df_2023 = get_weighted_dir(wind_dir_data_daily, wind_speed_data_daily)
weighted_df_2022 = get_weighted_dir(wind_dir_2022_data_daily, wind_speed_2022_data_daily)
weighted_df_2021 = get_weighted_dir(wind_dir_2021_data_daily, wind_speed_2021_data_daily)
weighted_df_2020 = get_weighted_dir(wind_dir_2020_data_daily, wind_speed_2020_data_daily)
# weighted_df = get_weighted_dir(wind_dir_ctrl_data_daily, wind_speed_ctrl_data_daily)
# print(weighted_df)

output_dir = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\output"
export_path = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\output\flint_windrose.xlsx"   
export_path_2022 = r"S:\ExposureScienceLab\Flint Maternal Health Study\windrose\output\flint_windrose_2022.xlsx"        
create_windrose(weighted_df_2023, pm_data_daily, weighted_df_2022, pm_2022_data_daily, output_dir, export_path)
create_transparent_windrose(weighted_df_2020, pm_2020_data_daily, weighted_df_2021, pm_2021_data_daily, weighted_df_2022, pm_2022_data_daily, weighted_df_2023, pm_data_daily)
create_transparent_windrose(weighted_df_2020, pm_2020_data_daily)

# tmp = create_windrose(weighted_df, pm_ctrl_data_daily)

############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

import pandas as pd
import folium
from sklearn.preprocessing import MinMaxScaler
from branca.element import Template, MacroElement
import os
import seaborn as sns
import matplotlib.colors

COLUMNS = ['SITE NAME', 'Facility Type', 'Emissions (Tons)', 'Latitude', 'Longitude', 'State-County']
SCALER = MinMaxScaler(feature_range=(500, 5000))

def create_df(xlsx_file, county):
    '''
    Description:
        - Creates a dataframe from the xlsx file
    Parameters:
        - xlsx_file: the path to the xlsx file containing emissions data
        - county: the name of the county
    Returns:
        - df: the dataframe containing emissions data
    '''
    try:
        df = pd.read_excel(xlsx_file, usecols=COLUMNS)
        # df = df[df['State-County'] == 'MI - Genesee']
        df = df[df['State-County'] == str(county)]
        df = df.drop(columns=['State-County'])
        df['Scaled Emissions'] = SCALER.fit_transform(df[['Emissions (Tons)']])
        print("Dataframe created")
        return df
    except Exception as e:
        print(e)
        return None

def create_color_dict(df):
    '''
    Description:
        - Creates a dictionary mapping facility types to colors
    Parameters:
        - df: the dataframe containing emissions data
    Returns:
        - color_dict: the dictionary mapping facility types to colors
    '''
    try:
        facility_types = df['Facility Type'].unique()
        colors = sns.hls_palette(len(facility_types))
        colors = [matplotlib.colors.rgb2hex(color) for color in colors]
        color_dict = dict(zip(facility_types, colors))
        print("Color dictionary created")
        return color_dict
    except Exception as e:
        print(e)
        return None

def create_emission_source_map(df):
    '''
    Description:
        - Uses the dataframe to create a map of locations with emissions data
        - It will first create a base map at the mean latitude and longitude of the data
        - Then it will create circles at each location with a radius proportional to the emissions
        - The map also includes a legend and a table of the top 5 sites with the highest emissions
    Parameters:
        - df: the dataframe containing emissions data
    Returns:
        - map_base: the map of emissions
    '''
    try:
        latitude = 43.047224
        longitude = -83.670159
        percentage = 0.01
        lower_latitude = 42.9901
        upper_latitude = 43.0970
        lower_longitude = -83.7762
        upper_longitude = -83.5641
        bounds = [[lower_latitude, lower_longitude], [upper_latitude, upper_longitude]]

        top_sites = df.nlargest(5, 'Emissions (Tons)')
        color_dict = create_color_dict(df)
        map_base = folium.Map(location=[latitude, longitude], zoom_start=11)

        image_group = folium.FeatureGroup(name='Image Overlay')
        folium.raster_layers.ImageOverlay(
            image=r'S:\ExposureScienceLab\Flint Maternal Health Study\windrose\output\transparent_windrose_2.png',
            bounds=bounds,
            opacity=1
        ).add_to(image_group)
        image_group.add_to(map_base)

        circle_group = folium.FeatureGroup(name='Circles')
        # folium.raster_layers.ImageOverlay(
        #     image=r'S:\ExposureScienceLab\Flint Maternal Health Study\windrose\output\transparent_windrose_2.png',
        #     bounds=bounds,
        #     opacity=1
        # ).add_to(map_base)

        for _, row in df.iterrows():
            folium.Circle(
                location=[row['Latitude'], row['Longitude']],
                radius=row['Scaled Emissions'],
                color=color_dict[row['Facility Type']],
                fill=True,
                popup=f"{row['SITE NAME']}, {row['Emissions (Tons)']} tons",
                tooltip=row['SITE NAME'],
            ).add_to(circle_group)

        circle_group.add_to(map_base)
        folium.LayerControl().add_to(map_base)

        map_base.add_child(folium.LatLngPopup())
        
        table_html = """
        <table style="width:100%">
            <tr>
                <th>Site Name</th>
                <th>Emissions (tons)</th>
            </tr>
        """

        for _, row in top_sites.iterrows():
            table_html += f"<tr><td>{row['SITE NAME']}</td><td>{row['Emissions (Tons)']}</td></tr>"
        table_html += "</table>"

        template = """
        {% macro html(this, kwargs) %}
        <div style="
            padding: 15px;
            position: fixed; 
            top: 5vh;
            left: 5vw;
            width: auto;
            height: auto;
            max-width: 30vw;
            max-height: 40vh;
            overflow: auto;
            z-index:9999;
            font-size:14px;
            background-color: #ffffff;
            ">
            <button onclick="toggleTable()">Show Top 5 Emissions Sites</button>
            <div id="tableDiv" style="display: none;">
                """ + table_html + """
            </div>
            <hr style="border: 0.3px solid #808080;">
            <p><a style="color:#808080;font-size:150%;">Facility Type</a></p>
            <hr style="border: 0.3px solid #808080;">
            {% for key in this.color_dict.keys() %}
            <p><i class="fa fa-circle fa-1x" style="color:{{this.color_dict[key]}};"></i> {{key}}</p>
            {% endfor %}
        </div>
        <script>
        function toggleTable() {
            var x = document.getElementById("tableDiv");
            if (x.style.display === "none") {
                x.style.display = "block";
            } else {
                x.style.display = "none";
            }
        }
        </script>
        {% endmacro %}
        """
        macro = MacroElement()
        macro._template = Template(template)
        macro.color_dict = color_dict
        full_map = map_base.get_root().add_child(macro)
        print("Map created")
        return full_map
    
    except Exception as e:
        print(e)
        return None

# note that most up to date data for facility emissions of pm2.5 is from 2020
input_xlsx_path = r"S:\ExposureScienceLab\Other\Emissions Maps\Genesee Facility Data Emissions.xlsx"
df = create_df(input_xlsx_path, 'MI - Genesee')
map = create_emission_source_map(df)
map.save(r'S:\ExposureScienceLab\Flint Maternal Health Study\windrose\output\flint_windrose_map_final.html')

############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################