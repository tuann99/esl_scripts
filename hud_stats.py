from scipy.stats import shapiro
import pandas as pd

path = r'S:\ExposureScienceLab\Lead Dust\Data\Master Sheets\RLDE Master Excel.xlsx'
df = pd.read_excel(path, sheet_name='python')
print(df.head())

shapiro_df = pd.DataFrame(columns=['visit', 'raw_stat', 'raw_pval', 'log_stat', 'log_pval', 'sample_type'])
print(shapiro_df)
print(shapiro_df.dtypes)

for visit in df['visit'].unique():
    print(f'on visit: {visit}')
    for x in df['sample_type'].unique():
        print(f'on sample type: {x}')
        raw_shapiro_test = shapiro(df.loc[(df['visit'] == visit) & (df['sample_type'] == x), 'raw'])
        log_shapiro_test = shapiro(df.loc[(df['visit'] == visit) & (df['sample_type'] == x), 'log'])

        tmp = {
        'visit': visit,
        'raw_stat': raw_shapiro_test.statistic,
        'raw_pval': raw_shapiro_test.pvalue,
        'log_stat': log_shapiro_test.statistic,
        'log_pval': log_shapiro_test.pvalue,
        'sample_type': x
        }

        shapiro_df = pd.concat([shapiro_df, pd.DataFrame(tmp, index=[0])])
print(shapiro_df)

##########################################################################################################
##########################################################################################################
##########################################################################################################
from scipy.stats import shapiro
import pandas as pd
import matplotlib.pyplot as plt

def outlier_removal(df, col, method, multiplier):
    if method == 'iqr':
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + multiplier * IQR
        lower_bound = Q1 - multiplier * IQR
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
    elif method == 'stdev':
        mean = df[col].mean()
        stdev = df[col].std()
        upper_bound = mean + multiplier * stdev
        lower_bound = mean - multiplier * stdev
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
    return df

path = r"S:\ExposureScienceLab\Pb Project Matthias\testing\soil_stats.xlsx"
pra_run_1 = pd.read_excel(path, sheet_name='pra_run_1')
pra_run_2 = pd.read_excel(path, sheet_name='pra_run_2')
log_pra_run_1 = pd.read_excel(path, sheet_name='log_pra_run_1')
log_pra_run_2 = pd.read_excel(path, sheet_name='log_pra_run_2')

stats_df_raw = pd.DataFrame(columns=['run_id', 'element', 'raw_stat', 'raw_pval', 'log_stat', 'log_pval'])
stats_df_iqr = pd.DataFrame(columns=['run_id', 'element', 'raw_stat', 'raw_pval', 'log_stat', 'log_pval'])
stats_df_stdev = pd.DataFrame(columns=['run_id', 'element', 'raw_stat', 'raw_pval', 'log_stat', 'log_pval'])
pra_data = pd.read_excel(path, sheet_name=None)
for sheet in pra_data.keys():
    if "log" in sheet or "." in sheet:
        continue
    print(f'On run: {sheet}')
    tmp = pd.read_excel(path, sheet_name=sheet)
    tmp_log = pd.read_excel(path, sheet_name=f'log_{sheet}')

    for colname in tmp.columns[1:]:
        element = colname.split('(')[0]
        print(f'On element: {element}')
        
        raw_stat, raw_pval = shapiro(tmp[colname])
        log_stat, log_pval = shapiro(tmp_log[colname])
        stats_df_raw = pd.concat([stats_df_raw, pd.DataFrame([{'run_id': sheet, 'element':colname, 
                                               'raw_stat':raw_stat,'raw_pval':raw_pval, 
                                               'log_stat': log_stat, 'log_pval':log_pval}], 
                                              index=[0])], ignore_index=True)
        
        tmp_iqr = outlier_removal(tmp, colname, 'iqr', 1.5)
        tmp_log_iqr = outlier_removal(tmp_log, colname, 'iqr', 1.5)
        raw_stat_iqr, raw_pval_iqr = shapiro(tmp_iqr[colname])
        log_stat_iqr, log_pval_iqr = shapiro(tmp_log_iqr[colname])
        stats_df_iqr = pd.concat([stats_df_iqr, pd.DataFrame([{'run_id': sheet, 'element':colname, 
                                               'raw_stat':raw_stat_iqr,'raw_pval':raw_pval_iqr, 
                                               'log_stat': log_stat_iqr, 'log_pval':log_pval_iqr}], 
                                              index=[0])], ignore_index=True)
        
        tmp_stdev = outlier_removal(tmp, colname, 'stdev', 2)
        tmp_log_stdev = outlier_removal(tmp_log, colname, 'stdev', 2)
        raw_stat_stdev, raw_pval_stdev = shapiro(tmp_stdev[colname])
        log_stat_stdev, log_pval_stdev = shapiro(tmp_log_stdev[colname])
        stats_df_stdev = pd.concat([stats_df_stdev, pd.DataFrame([{'run_id': sheet, 'element':colname, 
                                               'raw_stat':raw_stat_stdev,'raw_pval':raw_pval_stdev, 
                                               'log_stat': log_stat_stdev, 'log_pval':log_pval_stdev}], 
                                              index=[0])], ignore_index=True)

        print(f"""
Run: {sheet}
Number of {element} values in raw data: {len(tmp)}
Number of {element} values in IQR data: {len(tmp_iqr)}
Number of {element} values in STDev data: {len(tmp_stdev)}
              """)

print(stats_df_raw)
print(stats_df_iqr)
print(stats_df_stdev)
##########################################################################################################
##########################################################################################################
##########################################################################################################
# now perform t-tests on the data
from scipy.stats import ttest_ind
 
pra_data = pd.read_excel(path, sheet_name=None)
ttest_results = pd.DataFrame(
    columns=['run_id', 'element', 
             'raw_stat', 'raw_pval', 
             'log_stat', 'log_pval', 
             'raw_iqr_stat', 'raw_iqr_pval', 
             'log_iqr_stat', 'log_iqr_pval'])
for sheet in ['pra_run_1', 'pra_run_2']:
    print(f'On run: {sheet}')
    tmp = pd.read_excel(path, sheet_name=sheet)
    tmp_log = pd.read_excel(path, sheet_name=f'log_{sheet}')

    for place in ['ja', 'ba', 'msu']:
        tmp_place_df = pd.read_excel(path, sheet_name=f'{place}')
        tmp_log_place_df = pd.read_excel(path, sheet_name=f'log_{place}')
        print(f'On place: {place}')
        for colname in tmp.columns[1:]:
            element = colname.split('(')[0]
            print(f'On element: {element}')

            ttest_raw = ttest_ind(tmp[colname], tmp_place_df[colname], equal_var=False)
            ttest_log = ttest_ind(tmp_log[colname], tmp_log_place_df[colname], equal_var=False)
            ttest_raw_iqr = ttest_ind(outlier_removal(tmp, colname, 'iqr', 1.5)[colname], outlier_removal(tmp_place_df, colname, 'iqr', 1.5)[colname], equal_var=False)
            ttest_log_iqr = ttest_ind(outlier_removal(tmp_log, colname, 'iqr', 1.5)[colname], outlier_removal(tmp_log_place_df, colname, 'iqr', 1.5)[colname], equal_var=False)

            ttest_results = pd.concat([ttest_results, pd.DataFrame([{'run_id': sheet, 'tested_against':place,'element':colname, 
                                                   'raw_stat':ttest_raw.statistic,'raw_pval':ttest_raw.pvalue, 
                                                   'log_stat': ttest_log.statistic, 'log_pval':ttest_log.pvalue,
                                                   'raw_iqr_stat':ttest_raw_iqr.statistic,'raw_iqr_pval':ttest_raw_iqr.pvalue, 
                                                   'log_iqr_stat': ttest_log_iqr.statistic, 'log_iqr_pval':ttest_log_iqr.pvalue}], 
                                                  index=[0])], ignore_index=True)

print(ttest_results)

##########################################################################################################
##########################################################################################################
##########################################################################################################
# --------------------------------------------------------------------------------------- #
# first check if Pb in PRA is normally distributed w shapiro
print(shapiro(pra_run_1['Pb208(LR)']))
# ShapiroResult(statistic=0.25349903106689453, pvalue=1.253637749165648e-09)
# so raw Pb is def not normally distributed
# here is what hist looks like
plt.hist(pra_run_1['Pb208(LR)'])
plt.show()

# --------------------------------------------------------------------------------------- #
# now gotta check how removing outliers from raw data via IQR and STDev does
# iqr first
Q1 = pra_run_1['Pb208(LR)'].quantile(0.25)
Q3 = pra_run_1['Pb208(LR)'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR
lower_bound = Q1 - 1.5 * IQR
print(f"""
Q1: {Q1}
Q3: {Q3}
IQR: {IQR}
upper_bound: {upper_bound}
lower_bound: {lower_bound}
      """)

pra_run_1_iqr = pra_run_1[(pra_run_1['Pb208(LR)'] > lower_bound) & (pra_run_1['Pb208(LR)'] < upper_bound)]
print(shapiro(pra_run_1_iqr['Pb208(LR)']))
# ShapiroResult(statistic=0.9322748780250549, pvalue=0.2128908634185791)
# Removing outliers via IQR makes Pb208(LR) normally distributed
plt.hist(pra_run_1_iqr['Pb208(LR)'])
plt.show()

# --------------------------------------------------------------------------------------- #
# now stdev
mean = pra_run_1['Pb208(LR)'].mean()
stdev = pra_run_1['Pb208(LR)'].std()
upper_bound = mean + 2 * stdev
lower_bound = mean - 2 * stdev
print(f"""
mean: {mean}
stdev: {stdev}
upper_bound: {upper_bound}
lower_bound: {lower_bound}
      """)
pra_run_1_stdev = pra_run_1[(pra_run_1['Pb208(LR)'] > lower_bound) & (pra_run_1['Pb208(LR)'] < upper_bound)]
print(shapiro(pra_run_1_stdev['Pb208(LR)']))
# ShapiroResult(statistic=0.8396207094192505, pvalue=0.0028288974426686764) # Removing outliers via 2*STDev does not make Pb208(LR) normally distributed
# ShapiroResult(statistic=0.8396207094192505, pvalue=0.0028288974426686764) # Removing outliers via 2.5*STDev does not make Pb208(LR) normally distributed
plt.hist(pra_run_1_stdev['Pb208(LR)'])
plt.show()

# --------------------------------------------------------------------------------------- #
print(shapiro(pra_run_1['Al27(MR)']))
# ShapiroResult(statistic=0.9628510475158691, pvalue=0.5489694476127625)
# so raw Al is normally distributed

# --------------------------------------------------------------------------------------- #
# now gotta check how removing outliers from raw data via IQR and STDev does
# iqr first
Q1 = pra_run_1['Al27(MR)'].quantile(0.25)
Q3 = pra_run_1['Al27(MR)'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR
lower_bound = Q1 - 1.5 * IQR
print(f"""
Q1: {Q1}
Q3: {Q3}
IQR: {IQR}
upper_bound: {upper_bound}
lower_bound: {lower_bound}
      """)
pra_run_1_iqr_al = pra_run_1[(pra_run_1['Al27(MR)'] > lower_bound) & (pra_run_1['Al27(MR)'] < upper_bound)]
print(shapiro(pra_run_1_iqr_al['Al27(MR)']))
# ShapiroResult(statistic=0.9628510475158691, pvalue=0.5489694476127625)
# Removing outliers via IQR still has Al27(MR) normally distributed

# --------------------------------------------------------------------------------------- #
# now stdev
mean = pra_run_1['Al27(MR)'].mean()
stdev = pra_run_1['Al27(MR)'].std()
upper_bound = mean + 2 * stdev
lower_bound = mean - 2 * stdev
print(f"""
mean: {mean}
stdev: {stdev}
upper_bound: {upper_bound}
lower_bound: {lower_bound}
      """)
pra_run_1_stdev_al = pra_run_1[(pra_run_1['Al27(MR)'] > lower_bound) & (pra_run_1['Al27(MR)'] < upper_bound)]
print(shapiro(pra_run_1_stdev_al['Al27(MR)']))
# ShapiroResult(statistic=0.9725245833396912, pvalue=0.7880703210830688) # Removing outliers via 2*STDev still has Al27(MR) normally distributed
# ShapiroResult(statistic=0.9628510475158691, pvalue=0.5489694476127625) # Removing outliers via 2.5*STDev still has Al27(MR) normally distributed

# --------------------------------------------------------------------------------------- #
print(shapiro(pra_run_1['Cu63(MR)']))
# ShapiroResult(statistic=0.8425018191337585, pvalue=0.002508719451725483)
# so raw Cu is not normally distributed

# --------------------------------------------------------------------------------------- #
# now gotta check how removing outliers from raw data via IQR and STDev does
# iqr first
pra_run_1_iqr_cu = outlier_removal(pra_run_1, 'Cu63(MR)', 'iqr', 1.5)
print(shapiro(pra_run_1_iqr_cu['Cu63(MR)']))
# ShapiroResult(statistic=0.8558483719825745, pvalue=0.006690125446766615)
# Removing outliers via IQR does not make Cu63(MR) normally distributed

# --------------------------------------------------------------------------------------- #
# now stdev
pra_run_1_stdev_cu = outlier_removal(pra_run_1, 'Cu63(MR)', 'stdev', 2.5)
print(shapiro(pra_run_1_stdev_cu['Cu63(MR)']))
# ShapiroResult(statistic=0.8558483719825745, pvalue=0.006690125446766615) # Removing outliers via 2*STDev does not make Cu63(MR) normally distributed
# ShapiroResult(statistic=0.8425018191337585, pvalue=0.002508719451725483) # Removing outliers via 2.5*STDev does not make Cu63(MR) normally distributed

# --------------------------------------------------------------------------------------- #
print(shapiro(pra_run_2['Pb208(LR)']))
# ShapiroResult(statistic=0.25723540782928467, pvalue=1.334121035867497e-09)
# raw Pb is not normally distributed in second run

# --------------------------------------------------------------------------------------- #
# now gotta check how removing outliers from raw data via IQR and STDev does
# iqr first
pra_run_2_iqr = outlier_removal(pra_run_2, 'Pb208(LR)', 'iqr', 1.5)
print(shapiro(pra_run_2_iqr['Pb208(LR)']))
# ShapiroResult(statistic=0.9871876835823059, pvalue=0.9919033646583557)
# Removing outliers via IQR makes Pb208(LR) normally distributed

# --------------------------------------------------------------------------------------- #
# now stdev
pra_run_2_stdev = outlier_removal(pra_run_2, 'Pb208(LR)', 'stdev', 2.5)
print(shapiro(pra_run_2_stdev['Pb208(LR)']))
# ShapiroResult(statistic=0.9291179776191711, pvalue=0.13215939700603485) # Removing outliers via 2*STDev makes Pb208(LR) normally distributed
# ShapiroResult(statistic=0.9291179776191711, pvalue=0.13215939700603485) # Removing outliers via 2.5*STDev is same as 2*STDev

# --------------------------------------------------------------------------------------- #
print(shapiro(pra_run_2['Cu63(MR)']))
# ShapiroResult(statistic=0.8819527626037598, pvalue=0.013166449964046478)
# raw Cu is not normally distributed in second run

# --------------------------------------------------------------------------------------- #
# now gotta check how removing outliers from raw data via IQR and STDev does
# iqr first
pra_run_2_iqr_cu = outlier_removal(pra_run_2, 'Cu63(MR)', 'iqr', 1.5)
print(shapiro(pra_run_2_iqr_cu['Cu63(MR)']))
# ShapiroResult(statistic=0.8819527626037598, pvalue=0.013166449964046478) # Removing outliers via IQR does not make Cu63(MR) normally distributed

# --------------------------------------------------------------------------------------- #
# now stdev
pra_run_2_stdev_cu = outlier_removal(pra_run_2, 'Cu63(MR)', 'stdev', 2)
print(shapiro(pra_run_2_stdev_cu['Cu63(MR)']))
# ShapiroResult(statistic=0.8853000402450562, pvalue=0.018341481685638428) # Removing outliers via 2*STDev does not make Cu63(MR) normally distributed
# ShapiroResult(statistic=0.8819527626037598, pvalue=0.013166449964046478) # Removing outliers via 2.5*STDev does not make Cu63(MR) normally distributed

# --------------------------------------------------------------------------------------- #
# now checking log transformed data
print(shapiro(log_pra_run_1['Pb208(LR)']))
# ShapiroResult(statistic=0.5089942216873169, pvalue=1.5981044043655857e-07) # log transformed Pb is not normally distributed

# --------------------------------------------------------------------------------------- #
# now gotta check how removing outliers from log transformed data via IQR and STDev does
log_pra_run_1_iqr = outlier_removal(log_pra_run_1, 'Pb208(LR)', 'iqr', 1.5)
print(shapiro(log_pra_run_1_iqr['Pb208(LR)']))
# ShapiroResult(statistic=0.9257164001464844, pvalue=0.16318655014038086) # Removing outliers via IQR makes log transformed Pb normally distributed

log_pra_run_1_stdev = outlier_removal(log_pra_run_1, 'Pb208(LR)', 'stdev', 2.5)
print(shapiro(log_pra_run_1_stdev['Pb208(LR)']))
# ShapiroResult(statistic=0.9359431266784668, pvalue=0.18100084364414215) # Removing outliers via 2*STDev makes log transformed Pb normally distributed
# ShapiroResult(statistic=0.9359431266784668, pvalue=0.18100084364414215) # Removing outliers via 2.5*STDev is same as 2*STDev

# --------------------------------------------------------------------------------------- #
print(shapiro(log_pra_run_1['Cu63(MR)']))
# ShapiroResult(statistic=0.8617871999740601, pvalue=0.005525919608771801) # log transformed Cu is not normally distributed

# --------------------------------------------------------------------------------------- #
# now gotta check how removing outliers from log transformed data via IQR and STDev does
log_pra_run_1_iqr_cu = outlier_removal(log_pra_run_1, 'Cu63(MR)', 'iqr', 1.5)
print(shapiro(log_pra_run_1_iqr_cu['Cu63(MR)']))
# ShapiroResult(statistic=0.9582083821296692, pvalue=0.48079657554626465) # Removing outliers via IQR makes log transformed Cu normally distributed

log_pra_run_1_stdev_cu = outlier_removal(log_pra_run_1, 'Cu63(MR)', 'stdev', 2.5)
print(shapiro(log_pra_run_1_stdev_cu['Cu63(MR)']))
# ShapiroResult(statistic=0.9582083821296692, pvalue=0.48079657554626465) # Removing outliers via 2*STDev makes log transformed Cu normally distributed
# ShapiroResult(statistic=0.9582083821296692, pvalue=0.48079657554626465) # Removing outliers via 2.5*STDev is same as 2*STDev

# --------------------------------------------------------------------------------------- #
print(shapiro(log_pra_run_1['Al27(MR)']))
# ShapiroResult(statistic=0.9303389191627502, pvalue=0.12470782548189163) # log transformed Al is normally distributed

# --------------------------------------------------------------------------------------- #
# now gotta check how removing outliers from log transformed data via IQR and STDev does
log_pra_run_1_iqr_al = outlier_removal(log_pra_run_1, 'Al27(MR)', 'iqr', 1.5)
print(shapiro(log_pra_run_1_iqr_al['Al27(MR)']))
# ShapiroResult(statistic=0.9303389191627502, pvalue=0.12470782548189163) # Removing outliers via IQR still has log transformed Al normally distributed

log_pra_run_1_stdev_al = outlier_removal(log_pra_run_1, 'Al27(MR)', 'stdev', 2)
print(shapiro(log_pra_run_1_stdev_al['Al27(MR)']))
# ShapiroResult(statistic=0.9569745063781738, pvalue=0.48531827330589294) # Removing outliers via 2*STDev still has log transformed Al normally distributed
# ShapiroResult(statistic=0.9303389191627502, pvalue=0.12470782548189163) # Removing outliers via 2.5*STDev still has log transformed Al normally distributed

# --------------------------------------------------------------------------------------- #
print(shapiro(log_pra_run_2['Pb208(LR)']))
# ShapiroResult(statistic=0.5352925062179565, pvalue=2.868395085897646e-07) # log transformed Pb is not normally distributed

# --------------------------------------------------------------------------------------- #
# now gotta check how removing outliers from log transformed data via IQR and STDev does
log_pra_run_2_iqr = outlier_removal(log_pra_run_2, 'Pb208(LR)', 'iqr', 1.5)
print(shapiro(log_pra_run_2_iqr['Pb208(LR)']))
# ShapiroResult(statistic=0.9824381470680237, pvalue=0.9558619856834412) # Removing outliers via IQR makes log transformed Pb normally distributed

log_pra_run_2_stdev = outlier_removal(log_pra_run_2, 'Pb208(LR)', 'stdev', 2.5)
print(shapiro(log_pra_run_2_stdev['Pb208(LR)']))
# ShapiroResult(statistic=0.9824381470680237, pvalue=0.9558619856834412) # Removing outliers via 2*STDev makes log transformed Pb normally distributed
# ShapiroResult(statistic=0.9824381470680237, pvalue=0.9558619856834412) # Removing outliers via 2.5*STDev is same as 2*STDev

# --------------------------------------------------------------------------------------- #
# Summary: 