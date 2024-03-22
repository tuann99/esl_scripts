import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# from datetime import datetime
import datetime
import sqlite3 as sql
import os

def remove_outliers_z_score(df, column):
    z_scores = (df[column] - df[column].mean()) / df[column].std()
    return df[(np.abs(z_scores) < 3)]

def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    return df[~((df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR)))]

def time_to_seconds(time):
    return (time.hour * 60 + time.minute) * 60 + time.second

def data_formatting(df):
    # add the units to the column names
    df.columns = df.columns.map(lambda x: f'{x[0]} ({x[1]})' if pd.notna(x[1]) and not 'Unnamed' in x[1] else x[0])

    # format Timestamp (UTC) column as datetime
    df['Timestamp (UTC)'] = pd.to_datetime(df['Timestamp (UTC)'])
    df['Timestamp (UTC)']

    # change from utc to est
    df_tmp = df.copy()
    df_tmp['Timestamp (EST)'] = df_tmp['Timestamp (UTC)'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')

    # separate date and time into separate columns. Doing this to validate the time conversion
    df_tmp['Date (UTC)'] = df_tmp['Timestamp (UTC)'].dt.date
    df_tmp['Times (UTC)'] = df_tmp['Timestamp (UTC)'].dt.time

    df_tmp['Date (EST)'] = df_tmp['Timestamp (EST)'].dt.date
    df_tmp['Times (EST)'] = df_tmp['Timestamp (EST)'].dt.time

    # label data with before and after turning on AFU. so before 2/22/2024 13:15 is labeled as "before afu on" and that 
    # point and after is labeled as "after afu on"
    df_tmp['afu_status'] = np.where(df_tmp['Timestamp (UTC)'] < datetime(2024, 2, 22, 13, 15), 'before afu on', 'after afu on')
    df_tmp[df_tmp['afu_status'] == 'before afu on']
    df_tmp[df_tmp['afu_status'] == 'after afu on']

    return df_tmp

db = r"S:\ExposureScienceLab\Other\voc_testing\voc_testing.db"
export_dir = r"S:\ExposureScienceLab\Other\voc_testing\other_data"
wkdir = r"S:\ExposureScienceLab\Other\voc_testing"

#####################################################################################################################
#####################################################################################################################
################################################## Create DB ########################################################
#####################################################################################################################
#####################################################################################################################

conn = sql.connect(db)
c = conn.cursor()




#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################



#####################################################################################################################
#####################################################################################################################
########################################### Data Cleaning/Formatting ################################################
#####################################################################################################################
#####################################################################################################################

# make a check to see if the data is already in the database

for file in os.listdir(wkdir):
    # file is formatted as "YYYY_MM_DD_airassure_[afu or baseline]_###.csv"
    if file.endswith(".csv"):
        print(file)
        # check if the file is already in the database by the ### part of the file name
        c.execute(f"SELECT * FROM airassure_afu WHERE file_name LIKE '%{file[-7:-4]}%'")
        if c.fetchone() is not None:
            print(f"{file} is already in the database")
        else:
            print(f"{file} is not in the database")
            dat = os.path.join(wkdir, file)
            df = pd.read_csv(dat, comment="#", header=[0, 1])

dat = r"S:\ExposureScienceLab\Other\voc_testing\2024_02_23_airassure_afu.csv"
df = pd.read_csv(dat, comment="#", header=[0, 1])

# add the units to the column names
df.columns = df.columns.map(lambda x: f'{x[0]} ({x[1]})' if pd.notna(x[1]) and not 'Unnamed' in x[1] else x[0])
print(df.columns)

# format Timestamp (UTC) column as datetime
df['Timestamp (UTC)'] = pd.to_datetime(df['Timestamp (UTC)'])
df['Timestamp (UTC)']

# change from utc to est
df_tmp = df.copy()
df_tmp['Timestamp (EST)'] = df_tmp['Timestamp (UTC)'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')

# separate date and time into separate columns. Doing this to validate the time conversion
df_tmp['Date (UTC)'] = df_tmp['Timestamp (UTC)'].dt.date
df_tmp['Times (UTC)'] = df_tmp['Timestamp (UTC)'].dt.time

df_tmp['Date (EST)'] = df_tmp['Timestamp (EST)'].dt.date
df_tmp['Times (EST)'] = df_tmp['Timestamp (EST)'].dt.time

# label data with before and after turning on AFU. so before 2/22/2024 13:15 is labeled as "before afu on" and that 
# point and after is labeled as "after afu on"
df_tmp['afu_status'] = np.where(df_tmp['Timestamp (UTC)'] < datetime(2024, 2, 22, 13, 15), 'before afu on', 'after afu on')
df_tmp[df_tmp['afu_status'] == 'before afu on']
df_tmp[df_tmp['afu_status'] == 'after afu on']

# add the id of the file to the dataframe

# add data to db
df_tmp.to_sql('airassure_afu', conn, if_exists='replace', index=False)
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################



#####################################################################################################################
#####################################################################################################################
################################################ Data Analysis ######################################################
#####################################################################################################################
#####################################################################################################################

# get tVOC (mg/m3) averages for each day with and without outliers
raw_df = df_tmp.copy()

for date in df_tmp['Timestamp (EST)'].dt.date.unique():

    # create a dataframe for each date
    date_df = df_tmp[df_tmp['Timestamp (EST)'].dt.date == date]
    date_df = date_df[['Date (UTC)', 'Date (EST)', 'Times (UTC)', 'Times (EST)', 'tVOC (mg/m3)']]
    print(date_df)

    # with outliers
    print(f"Summary stats with outliers from {date} ")
    print(date_df[date_df['Date (EST)'] == date]['tVOC (mg/m3)'].describe())
    # export to csv
    date_df.to_csv(f"{export_dir}/{date}_raw.csv", index=False)

    # without outliers (calculated from z-scores)
    print(f"Summary stats without outliers (calculated from z-scores) for data from {date}")
    df_no_outliers_z_score = remove_outliers_z_score(date_df, "tVOC (mg/m3)")
    print(df_no_outliers_z_score['tVOC (mg/m3)'].describe())
    # export to csv
    df_no_outliers_z_score.to_csv(f"{export_dir}/{date}_no_outliers_z_score.csv", index=False)

    # without outliers (calculated from IQR)
    print(f"Summary stats without outliers (calculated from IQR) for data from {date}")
    df_no_outliers_iqr = remove_outliers_iqr(date_df, "tVOC (mg/m3)")
    print(df_no_outliers_iqr['tVOC (mg/m3)'].describe())
    # export to csv
    df_no_outliers_iqr.to_csv(f"{export_dir}/{date}_no_outliers_iqr.csv", index=False)

# get tVOC (mg/m3) averages for before and after turning on AFU with and without outliers
for afu_status in df_tmp['afu_status'].unique():

    # create a dataframe for each afu_status
    afu_status_df = df_tmp[df_tmp['afu_status'] == afu_status]
    afu_status_df = afu_status_df[['Date (UTC)', 'Date (EST)', 'Times (UTC)', 'Times (EST)', 'tVOC (mg/m3)']]
    print(afu_status_df)

    # with outliers
    print(f"Summary stats with outliers for {afu_status} ")
    print(afu_status_df['tVOC (mg/m3)'].describe())
    # export to csv
    afu_status_df.to_csv(f"{export_dir}/{afu_status}_raw.csv", index=False)

    # without outliers (calculated from z-scores)
    print(f"Summary stats without outliers (calculated from z-scores) for data from {afu_status}")
    df_no_outliers_z_score = remove_outliers_z_score(afu_status_df, "tVOC (mg/m3)")
    print(df_no_outliers_z_score['tVOC (mg/m3)'].describe())
    # export to csv
    df_no_outliers_z_score.to_csv(f"{export_dir}/{afu_status}_no_outliers_z_score.csv", index=False)

    # without outliers (calculated from IQR)
    print(f"Summary stats without outliers (calculated from IQR) for data from {afu_status}")
    df_no_outliers_iqr = remove_outliers_iqr(afu_status_df, "tVOC (mg/m3)")
    print(df_no_outliers_iqr['tVOC (mg/m3)'].describe())
    # export to csv
    df_no_outliers_iqr.to_csv(f"{export_dir}/{afu_status}_no_outliers_iqr.csv", index=False)

# plot of tVOC (mg/m3) over time, with markers for afu status
fig, ax = plt.subplots()
for status in df_tmp['afu_status'].unique():
    status_df = df_tmp[df_tmp['afu_status'] == status]
    ax.plot(status_df['Timestamp (EST)'], status_df['tVOC (mg/m3)'], label=status)
    ax.set_xlabel('Time')
    ax.set_ylabel('tVOC (mg/m3)')
    ax.set_title('tVOC (mg/m3) over time')
    ax.legend()
plt.xticks([])
plt.show()

# plot of tVOC (mg/m3) over time, with markers for the start of each day
# plt.figure(figsize=(10, 5))
fig, ax = plt.subplots()

for date in df_tmp['Timestamp (EST)'].dt.date.unique():
    print(date)
    date_df = df_tmp[df_tmp['Timestamp (EST)'].dt.date == date]
    date_df.columns
    print(date_df)

    # date_df['Times (EST)'] = date_df['Times (EST)'].astype('str')
    date_df['Times (EST)'] = date_df['Times (EST)'].apply(time_to_seconds)
    
    ax.plot(date_df['Times (EST)'], date_df['tVOC (mg/m3)'], label=date)
    # ax.axis([date_df['Timestamp (EST)'].min(), date_df['Timestamp (EST)'].max()])
    ax.axvline(date, color='black', linestyle='--', alpha=0.5)
    # ax.text(date, -1, f'{date}', rotation=10, verticalalignment='bottom')
    ax.legend()

ax.set_xlabel('Time')
ax.set_ylabel('tVOC (mg/m3)')
ax.set_title('tVOC over time')
fig.autofmt_xdate()

# plt.xticks([])
# plt.xticks(rotation=45)
plt.show()

#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################