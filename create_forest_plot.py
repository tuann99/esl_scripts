import forestplot as fp
import pandas as pd
import matplotlib.pyplot as plt
import os

export_path = r"S:\ExposureScienceLab\PM Cognitive\Meta-analysis\plots\python_plots\20240321"
xlsx_path = r"S:\ExposureScienceLab\PM Cognitive\Meta-analysis\stats\stats.xlsx"
# sheet = "python"
# sheet = "python2"
sheet = "python3"
# sheet = "python4"
# sheet = "python5"

sections = {}
current_section = None
current_data = []

both = 0
group = 0
nothing = 0

def format_data(df):
    # Round p-value to 4 decimal places and have scientific notation
    # df_lt["p-value"] = df_lt["p-value"].apply(lambda x: '%.4e' % x)

    # format so that any p-value less than 0.0001 is shown as "<0.0001" and any p-value greater than 0.05 is shown as ">0.05"
    # df["p-value"] = df["p-value"].apply(lambda x: "<0.0001" if x < 0.0001 else ">0.05" if x > 0.05 else x)
    # df["p-value-str"] = df["p-value"].apply(lambda x: "<0.0001" if x < 0.0001 else ">0.05" if x > 0.05 else str(x))
    # df["p-value"] = df["p-value"].round(2)
    # df["p-value"]
    # df["n"] = df["n"].round(0)
    # df["Relative Weight (%)"] = df["Relative Weight (%)"].round(4)

    df["ll"] = df["ll"].round(4)
    df["ul"] = df["ul"].round(4)
    df["corr"] = df["corr"].round(4)
    df["CI"] = df["corr"].astype(str) + " (" + df["ll"].astype(str) + ", " + df["ul"].astype(str) + ")"
    df["study_name"] = df["study_name"].astype(str)
    if "group" in df.columns:
        df["group"] = df["group"].astype(str)
    else:
        pass
    if "model" in df.columns:
        df["model"] = df["model"].astype(str)
    else:
        pass
    return df

df = pd.read_excel(xlsx_path, sheet_name=sheet, header=None)
print(df)

for _, row in df.iterrows():
    first_cell = row[0]
    print(f"First cell: {first_cell}")
    if pd.isna(first_cell):
        continue
    if first_cell.startswith('##'): # End of a section
        print("double hash detected")
        if current_section:
            print(f"Current section: {current_section}")
            # sections[current_section] = pd.DataFrame(current_data[1:], columns=current_data[0])
            print(f"check for current data[1:] :{current_data[1:3]}")
            print(f"check for current data[0] :{current_data[0]}")

            section_df = pd.DataFrame(current_data[1:], columns=current_data[0])
            print("Created dataframe for section: ", current_section)
            print(section_df)
            section_df.columns
            
            print("Formatting data for section: ", current_section)
            section_df = format_data(section_df)
            print("Formatted data for section: ", current_section)
            
            section_df = section_df.dropna(axis=1, how='all')
            print("Dropped empty columns in section: ", current_section)
            print(section_df)
            
            if "group" in section_df.columns and "model" not in section_df.columns:
                print(f"Only \"group\" column found in section: {current_section}")
                group += 1
                fig, ax = fp.forestplot(
                    section_df,
                    estimate="corr",
                    ll="ll", hl="ul",
                    varlabel="study_name",
                    pval="p-value",
                    annote=["CI"],
                    annoteheaders=["Est. (95% Conf. Int.)"],
                    xlabel="Pearson correlation coefficient",
                    table=True,
                    groupvar="group",
                    color_alt_rows=True,
                    decimal_precision=4,
                    # flush=False,
                    **{'fontfamily': 'sans-serif',
                       'variable_header': "Study Name",
                       'threshold': '0.005, 0.01, 0.05',
                       'pval_extrapad': 0.1,
                        }
                    )
                print("Plotted forest plot for section: ", current_section)
            
            elif "group" in section_df.columns and "model" in section_df.columns:
                print(f"Both \"group\" and \"model\" column found in section: {current_section}")
                both += 1
                fig, ax = fp.forestplot(
                    section_df,
                    estimate="corr",
                    ll="ll", hl="ul",
                    varlabel="study_name",
                    pval="p-value",
                    annote=["CI"],
                    annoteheaders=["Est. (95% Conf. Int.)"],
                    xlabel="Pearson correlation coefficient",
                    table=True,
                    groupvar="group",
                    model_col="model",
                    modellabels=["Fixed Effect Model", "Random Effect Model"],
                    mcolor=["#CC6677", "#4477AA"],
                    color_alt_rows=True,
                    decimal_precision=4,
                    # flush=False,
                    **{'fontfamily': 'sans-serif',
                       'variable_header': "Study Name",
                       'threshold': '0.005, 0.01, 0.05',
                       'pval_extrapad': 0.1,
                        })
                print("Plotted forest plot for section: ", current_section)
                
            else:
                print("No groupings in the section: ", current_section)
                nothing += 1
                fig, ax = fp.forestplot(
                    section_df,
                    estimate="corr",
                    ll="ll", hl="ul",
                    varlabel="study_name",
                    pval="p-value",
                    annote=["CI"],
                    annoteheaders=["Est. (95% Conf. Int.)"],
                    xlabel="Pearson correlation coefficient",
                    table=True,
                    color_alt_rows=True,
                    decimal_precision=4,
                    # flush=False,
                    **{'fontfamily': 'sans-serif',
                       'variable_header': "Study Name",
                       'threshold': '0.005, 0.01, 0.05',
                       'pval_extrapad': 0.1,
                        }
                    )
                print("Plotted forest plot for section: ", current_section)
                
            tmp = current_section.replace(" ", "_")
            tmp = tmp.replace(",", "_")
            tmp = f"{tmp}.png"
            full_export_path = os.path.join(export_path, tmp)
            # plt.subplots_adjust(wspace=50, hspace=20)
            title = f"{current_section}"
            parts = title.split(",")
            if len(parts) > 1:
                # title = parts[0] + "\n" + parts[1]
                title = '\n'.join(parts)
                # print(f"Title with first method:\n{title}\nand second method:\n{title_2}")
            
            mid = (fig.subplotpars.right + fig.subplotpars.left)/2
            mid_ax = (ax.get_position().xmax + ax.get_position().xmin)/2
            mid_gcf = (plt.gcf().subplotpars.right + plt.gcf().subplotpars.left)/2
            print(f"left: {fig.subplotpars.left}, right: {fig.subplotpars.right}")
            print(f"mid point of fig: {mid}")
            print(f"ax.get_position().xmax: {ax.get_position().xmax}, ax.get_position().xmin: {ax.get_position().xmin}")
            print(f"mid point of ax: {mid_ax}")
            print(f"mid point of plt.gcf(): {mid_gcf}")
            # ax.set_title(title, fontsize=12, fontweight="bold", x=mid, y=1.05)
            # ax.set_title(title, fontsize=12, fontweight="bold", x=-0.055, y=1.10)
            ax.set_title(title, fontsize=12, fontweight="bold", x=0.15, y=1.10)
            # ax.set_title(f"{current_section}", fontsize=12, fontweight="bold", x=0)
            # plt.gcf().suptitle(title, fontsize=12, fontweight="bold", x=mid)
            # plt.gcf().suptitle(title_2, fontsize=12, fontweight="bold", x=-0.25)
            # plt.gcf().suptitle(f"{current_section}", fontsize=12, fontweight="bold", x=0) # this one was for 'Correlation Between PM2.5 Exposure And Cognitive Assessment Score' plot bc it was coming out weird. Use with sheet 'python2'
            plt.savefig(f"{full_export_path}", bbox_inches="tight", pad_inches=0.5)
            # plt.show()
            current_section = None
            current_data = []
    elif first_cell.startswith('#'):
        print("single hash detected")
        current_section = first_cell[1:].strip()
        print(f"this is the current section: {current_section}")
    else:
        print("Appending row to current data")
        current_data.append(row.values)

print(f"Both: {both}, Group: {group}, Nothing: {nothing}")

# This is in plot.py of forestplot module and controls the size of the fp itself
# figsize: Union[Tuple, List] = (7, 7),
# 