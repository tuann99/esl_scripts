#!usr/bin/env python3

########################################################################################################
# MSU Exposure Science Lab
# Author: Tuan Nguyen
# Purpose: Create an interactive map of emissions from xlsx files downkloaded from the EPA's website.
# Input: Path to the xlsx file containing emissions data, path to directory where you want to save the map
# Output: Map of emissions as an html file
# Requirements: Full list available in /venv_requirements/emissions-map-env-requirements.txt
# Usage: python path/to/create_emissions_map.py -i <input_xlsx_path> -o <output_dir>

import pandas as pd
import folium
from sklearn.preprocessing import MinMaxScaler
import argparse
from branca.element import Template, MacroElement
import os
import seaborn as sns
import matplotlib.colors

COLUMNS = ['SITE NAME', 'Facility Type', 'Emissions (Tons)', 'Latitude', 'Longitude', 'State-County']
SCALER = MinMaxScaler(feature_range=(500, 5000))

def create_df(xlsx_file):
    '''
    Description:
        - Creates a dataframe from the xlsx file
    Parameters:
        - xlsx_file: the path to the xlsx file containing emissions data
    Returns:
        - df: the dataframe containing emissions data
    '''
    try:
        df = pd.read_excel(xlsx_file, usecols=COLUMNS)
        df = df[df['State-County'] == 'MI - Genesee']
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

def create_map(df):
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
        top_sites = df.nlargest(5, 'Emissions (Tons)')
        color_dict = create_color_dict(df)
        map_base = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=11)

        for _, row in df.iterrows():
            folium.Circle(
                location=[row['Latitude'], row['Longitude']],
                radius=row['Scaled Emissions'],
                color=color_dict[row['Facility Type']],
                fill=True,
                popup=f"{row['SITE NAME']}, {row['Emissions (Tons)']} tons",
                tooltip=row['SITE NAME'],
            ).add_to(map_base)

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

def main():
    try:
        parser = argparse.ArgumentParser(description='Create a map of emissions')
        parser.add_argument('-i', '--input_xlsx_path', type=str, help='Path to the xlsx file containing emissions data')
        parser.add_argument('-o', '--output_dir', type=str, help='Path to directory where you want to save the map')
        args = parser.parse_args()
    except Exception as e:
        print(e)
        return None

    try:
        df = create_df(args.input_xlsx_path)
        map = create_map(df)
        output_path = os.path.join(args.output_dir, 'map.html')
        map.save(output_path)
        print("Map saved")
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    main()