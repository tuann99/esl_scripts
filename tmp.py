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