#!/usr/bin/env python

import geopandas as gpd
import folium
from shapely.ops import unary_union
from branca.element import Template, MacroElement
import os
import argparse

def create_map_base(latitude, longitude):
    """
    Description:
    Creates a base map centered around the location of interest

    Parameters:
    latitude: Latitude given in decimal degrees
    longitude: Longitude given in decimal degrees

    Returns:
    A base folium map
    """
    try:
        map = folium.Map(location=[latitude, longitude], min_zoom=10, zoom_start=13)

        if map is None:
            raise Exception("Map base not created successfully")
        else:
            print("Map base created successfully")
            return map
        
    except Exception as e:
        return f"An error occurred in creating the map base: {e}"

def create_df_and_format(road_json_path):
    """
    Description:
    Creates a geographical data frame, merges road coordinates to create a single road
    object, then converts coordinate reference system (CRS) into suitable one for mapping

    Parameters:
    road_json_path: The path to the json file containing the geographical info for roads

    Returns:
    GeoSeries of road data
    """
    try:
        road_data = fr"{road_json_path}"
        road_gdf = gpd.read_file(road_data)
        road_geometry = unary_union(road_gdf['geometry'])
        road_gs = gpd.GeoSeries([road_geometry], crs=road_gdf.crs)
        road_gs = road_gs.to_crs(epsg=3857) # WGS 84 / Pseudo-Mercator units = meters
        # EPSG:3174 (NAD83 / Great Lakes Albers) is one that is more focused on NA with units in meters too

        if road_gs is None:
            raise Exception("Data frame could not be created and/or formatted.")
        else:
            print("Data frame created and formatted successfully")
            return road_gs
        
    except Exception as e:
        return f"An error occurred in creating the data frame and formatting: {e}"
    
def create_style_function(color):
    """
    Description:
    Creates a style function for the buffer zones because style functions cannot be
    created within the GeoJson layer itself due to the need for a color parameter

    Parameters:
    color: The color of the buffer zone
    
    Returns:
    A style function for the buffer zone
    """
    def style_function(feature):    
        return {
            'color': str(color),
            'fillOpacity': 0.4,
            'weight': 0.5
        }
    return style_function

def create_map_final(map, area, road_gs, name, dir):
    """
    Description:
    Creates a geographical data frame, merges road coordinates to create a single road
    object, then converts coordinate reference system (CRS) into suitable one for mapping

    Parameters:
    map: Folium map base
    area: The path of the GeoJSON file containing border data
    road_json_path: The path to the json file containing the geographical info for roads
    name: Name for the output file
    dir: Output directory

    Returns:
    None
    """
    try:
        template = """
        {% macro html(this, kwargs) %}
        <div style="
            position: fixed; 
            top: 5vh;
            left: 5vw;
            padding: 10px;
            padding-right: 10px;
            z-index:9999;
            background-color: #ffffff;
            font-size:14px;
            ">
            <p><a style="color:#808080;font-size:150%;">Legend</a></p>
            <p><a style="color:#0000FF;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;Area Boundaries</p>
            <p><a style="color:#008000;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;500m Zone</p>
            <p><a style="color:#DC9E00;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;300m Zone</p>
            <p><a style="color:#FF0000;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;150m Zone</p>
        </div>
        {% endmacro %}
        """
        macro = MacroElement()
        macro._template = Template(template)
        map.get_root().add_child(macro)

        if folium.GeoJson(
            area,
            name='Area Boundaries',
            style_function=create_style_function('#0000FF'),
            tooltip=folium.GeoJsonTooltip(
                fields=['LABEL'],
                localize=True
            )
        ).add_to(map):
            print("Area boundaries added to map")
        else:
            raise Exception("Area boundaries could not be added to map")
                

        buffers = [500, 300, 150]
        colors = ['#008000', '#DC9E00', '#FF0000']
        print(f"There are {len(buffers)} buffers")
        
        for i in range(len(buffers)):
            print(f"Creating {buffers[i]}m buffer...")
            print(f"Current color: {colors[i]}")

            buffer = road_gs.buffer(buffers[i])
            
            if buffer is None:
                raise Exception(f"{buffers[i]}m buffer could not be created.")
            else:
                print(f"{buffers[i]}m buffer created successfully")
            
            
            if folium.GeoJson(
                    buffer,
                    name=f'{buffers[i]}m Zone', 
                    style_function=create_style_function(colors[i])
                    ).add_to(map):
                print(f"{buffers[i]}m buffer added to map")
            else:
                raise Exception(f"{buffers[i]}m buffer could not be added to map")

        if folium.LayerControl().add_to(map):
            print("Layer control added successfully")
        else:
            raise Exception("Layer control could not be added to map")
        
        output_path = os.path.join(dir, name)
        map.save(fr"{output_path}")
        print(fr"Map saved to: {output_path}")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        default_output_directory = os.path.join(script_dir, "output")
        defaults = {
            'output_directory': default_output_directory,
            'output_name': 'trap_risk_map.html'
        }
        
        parser = argparse.ArgumentParser(description="Create traffic related air pollution (TRAP) maps.")
        parser.add_argument("-lat","--latitude", type=float, help="Latitude of starting area of interest in decimal degrees.")
        parser.add_argument("-lon", "--longitude", type=float, help="Longitude of starting area of interest in decimal degrees.")
        parser.add_argument("-i", "--input_json", type=str, help="Path of the JSON file containing road data.")
        parser.add_argument("-n", "--output_name", type=str, default=defaults["output_name"], help="The name the user wants for their map.")
        parser.add_argument("-o", "--output_directory", type=str, default=defaults["output_directory"], help="The directory the user wants to save their map to.")
        parser.add_argument("-a", "--area", type=str, help="Path of the GeoJSON file containing border data.")
        
        args = parser.parse_args()
        args_dict = vars(args)

        for arg_name, arg_value in args_dict.items():
            print(f"{arg_name}: {arg_value}")
            if arg_value == defaults["output_directory"] or arg_value == defaults["output_name"]:
                print(f"Using default value for {arg_name}: {arg_value}")
         
        print("Creating map...")    
        map = create_map_base(args.latitude, args.longitude)
        road_gs = create_df_and_format(args.input_json)
        create_map_final(map, args.area, road_gs, args.output_name, args.output_directory)
        print("Map created successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    main()

# map = folium.Map(location=[42.9634, -85.6681], min_zoom=10, zoom_start=13)
# template = """
#     {% macro html(this, kwargs) %}
#     <div style="
#         position: fixed; 
#         top: 5vh;
#         left: 5vw;
#         padding: 10px;
#         padding-right: 10px;
#         z-index:9999;
#         background-color: #ffffff;
#         font-size:14px;
#         ">
#         <p><a style="color:#808080;font-size:150%;">Legend</a></p>
#         <p><a style="color:#0000FF;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;Zip code boundaries</p>
#         <p><a style="color:#008000;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;500m Zone</p>
#         <p><a style="color:#DC9E00;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;300m Zone</p>
#         <p><a style="color:#FF0000;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;150m Zone</p>
#     </div>
#     {% endmacro %}
#     """

# macro = MacroElement()
# macro._template = Template(template)
# map.get_root().add_child(macro)

# zip_code_data = r"C:\Users\tuann\github\esl_scripts\data\trap_map_data\zip_code_and_roads\GR_ZIP_Code_Boundaries.json"
# road_data = r"C:\Users\tuann\github\esl_scripts\data\trap_map_data\zip_code_and_roads\State_owned_roads_filtered.json"
# road_gdf = gpd.read_file(road_data)
# road_geometry = unary_union(road_gdf['geometry'])
# road_gs = gpd.GeoSeries([road_geometry], crs=road_gdf.crs)
# road_gs = road_gs.to_crs(epsg=3857) # WGS 84 / Pseudo-Mercator units = meters
# # EPSG:3174 (NAD83 / Great Lakes Albers) is one that is more focused on NA with units in meters too

# buffer_500m = road_gs.buffer(500)
# buffer_300m = road_gs.buffer(300)
# buffer_150m = road_gs.buffer(150)

# zip_code_layer = folium.GeoJson(
#     zip_code_data,
#     name='Zip code boundaries',
#     style_function=lambda feature: {
#         'color': '#0000FF',
#         'fillOpacity': 0.1,
#         'weight': 1,
#     },
#     tooltip=folium.GeoJsonTooltip(
#         fields=['BASENAME'],
#         aliases=['Zip Code:'],
#         localize=True
#     )
#     ).add_to(map)

# outer_area_layer = folium.GeoJson(
#     buffer_500m,
#     name='500m Zone', 
#     style_function=lambda feature: {
#         'color': '#008000',
#         'fillOpacity': 0.4,
#         'weight': 0.5
#     }
# ).add_to(map)

# middle_area_layer = folium.GeoJson(
#     buffer_300m,
#     name='300m Zone', 
#     style_function=lambda feature: {
#         'color': '#DC9E00',
#         'fillOpacity': 0.5,
#         'weight': 0.5
#     }
# ).add_to(map)

# inner_area_layer = folium.GeoJson(
#     buffer_150m,
#     name='150m Zone', 
#     style_function=lambda feature: {
#         'color': '#FF0000',
#         'fillOpacity': 0.3,
#         'weight': 0.5
#     }
# ).add_to(map)

# folium.LayerControl().add_to(map)

# map.save(r"C:\Users\tuann\github\esl_scripts\output\trap_map_2.html")