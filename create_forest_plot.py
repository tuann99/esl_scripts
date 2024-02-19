import forestplot as fp
import pandas as pd
import matplotlib.pyplot as plt

# path_1 = r"C:\Users\nguye620\github\esl_scripts\data\ma_data.xlsx"
# path_lt = r"C:\Users\nguye620\github\esl_scripts\data\ma_data_lt.xlsx"
path_lt = r"S:\ExposureScienceLab\PM Cognitive\Meta-analysis\stats\ma_data_lt.xlsx"
df_lt = pd.read_excel(path_lt)
df_lt.columns
df_lt["Study Name"]
df_lt["ll"] = df_lt["ll"].round(4)
df_lt["ul"] = df_lt["ul"].round(4)

# Round p-value to 4 decimal places and have scientific notation
# df_lt["p-value"] = df_lt["p-value"].apply(lambda x: '%.4e' % x)
df_lt["p-value"] = df_lt["p-value"].round(4)
df_lt["p-value"]
df_lt["corr"] = df_lt["corr"].round(2)
df_lt["n"] = df_lt["n"].round(0)
df_lt["Relative Weight (%)"] = df_lt["Relative Weight (%)"].round(2)

# CI into format 0.00 (0.00, 0.00)
df_lt["CI"] = df_lt["corr"].astype(str) + " (" + df_lt["ll"].astype(str) + ", " + df_lt["ul"].astype(str) + ")"
df_lt["CI"]

fp.forestplot(df_lt,
    estimate="corr",
    ll="ll", hl="ul",
    varlabel="Study Name",
    xlabel="Pearson Correlation Coefficient",
    pval="p-value",
    annote=["n", "CI"],
    annoteheaders=["N", "Est. (95% Conf. Int.)"],
    rightannote=["p-value", "Relative Weight (%)"],
    right_annoteheaders=["P-value", "Relative Weight (%)"],
    table=True,
    **{'fontfamily': 'sans-serif'}
    )

plt.savefig(r"S:\ExposureScienceLab\PM Cognitive\Meta-analysis\plots\python_plots\test_plot_lt.png", bbox_inches="tight", pad_inches=0.5)



path_st = r"S:\ExposureScienceLab\PM Cognitive\Meta-analysis\stats\ma_data_st.xlsx"
df_st = pd.read_excel(path_st)
df_st.columns

plot = fp.forestplot(df_st,
    estimate="corr",
    ll="ll", hl="ul",
    varlabel="Study Name",
    ylabel="Pearson Correlation Coefficient(95% Confidence Interval)",
    pval="p-value",
    )
plt.savefig(r"S:\ExposureScienceLab\PM Cognitive\Meta-analysis\python_plots\test_plot_st.jpg", bbox_inches="tight")