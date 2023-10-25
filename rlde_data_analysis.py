import pandas as pd
import numpy as np

subject_1_dw = [0.9768864, 0.90, 0.38]
subject_1_dw = np.around(subject_1_dw, decimals=2)
subject_2_dw = [33.8850768, 10.64, 15.66]
subject_2_dw = np.around(subject_2_dw, decimals=2)
subject_3_dw = [1.2217632, 1.53, 0.83]
subject_3_dw = np.around(subject_3_dw, decimals=2)
subject_4_dw = [2.67, 2.09, 1.15]

subject_1_tsp = [6.45, 0.63, 0.78]
subject_2_tsp = [8.21, 14.23, 4.89]
subject_3_tsp = [7.31, 35.55, 3.92]
subject_4_tsp= [17.15, 0.22, 0.53]

# create df for dust wipe data
dw_data = {'Subject 1': subject_1_dw,
           'Subject 2': subject_2_dw,
           'Subject 3': subject_3_dw,
           'Subject 4': subject_4_dw}
dw_df = pd.DataFrame(dw_data, index=['Initial', 'Mid', 'Final'])

# create df for pDR data
tsp_data = {'Subject 1': subject_1_tsp,
           'Subject 2': subject_2_tsp,
           'Subject 3': subject_3_tsp,
           'Subject 4': subject_4_tsp}
tsp_df = pd.DataFrame(tsp_data, index=['Initial', 'Mid', 'Final'])

# correlation between dust wipe and pDR data
corr = dw_df.corrwith(tsp_df, axis=1)
print(corr)

# pearson correlation test
from scipy.stats import pearsonr
for i, (dw, tsp) in enumerate(zip([subject_1_dw, subject_2_dw, subject_3_dw, subject_4_dw], [subject_1_tsp, subject_2_tsp, subject_3_tsp, subject_4_tsp])):
    corr, _ = pearsonr(dw, tsp)
    print(f'Pearson\'s correlation between DW and TSP for subject {i+1}: %.3f' % corr)

# spearman correlation test
from scipy.stats import spearmanr
for i, (dw, tsp) in enumerate(zip([subject_1_dw, subject_2_dw, subject_3_dw, subject_4_dw], [subject_1_tsp, subject_2_tsp, subject_3_tsp, subject_4_tsp])):
    corr, _ = spearmanr(dw, tsp)
    print(f'Spearman\'s correlation between DW and TSP for subject {i+1}: %.3f' % corr)