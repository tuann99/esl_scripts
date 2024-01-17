import geopandas as gpd
import folium
from shapely.ops import unary_union
from branca.element import Template, MacroElement

map = folium.Map(location=[42.9634, -85.6681], min_zoom=10, zoom_start=13)

zip_code_data = r"C:\Users\tuann\github\esl_scripts\data\trap_map_data\zip_code_and_roads\GR_ZIP_Code_Boundaries.json"
road_data = r"C:\Users\tuann\github\esl_scripts\data\trap_map_data\zip_code_and_roads\State_owned_roads_filtered.json"
road_gdf = gpd.read_file(road_data)
road_geometry = unary_union(road_gdf['geometry'])
road_gs = gpd.GeoSeries([road_geometry], crs=road_gdf.crs)
road_gs = road_gs.to_crs(epsg=3857)

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
    <p><a style="color:#0000FF;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;Zip code boundaries</p>
    <p><a style="color:#008000;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;500m Zone</p>
    <p><a style="color:#DC9E00;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;300m Zone</p>
    <p><a style="color:#FF0000;font-size:150%;margin-left:20px;">&#9679;</a>&emsp;150m Zone</p>
</div>
{% endmacro %}
"""

macro = MacroElement()
macro._template = Template(template)
map.get_root().add_child(macro)

buffer_500m = road_gs.buffer(500)
buffer_300m = road_gs.buffer(300)
buffer_150m = road_gs.buffer(150)

zip_code_layer = folium.GeoJson(
    zip_code_data,
    name='Zip code boundaries',
    style_function=lambda feature: {
        'color': '#0000FF',
        'fillOpacity': 0.1,
        'weight': 1,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['BASENAME'],
        aliases=['Zip Code:'],
        localize=True
    )
    ).add_to(map)

outer_area_layer = folium.GeoJson(
    buffer_500m,
    name='500m Zone', 
    style_function=lambda feature: {
        'color': '#008000',
        'fillOpacity': 0.4,
        'weight': 0.5
    }
).add_to(map)

middle_area_layer = folium.GeoJson(
    buffer_300m,
    name='300m Zone', 
    style_function=lambda feature: {
        'color': '#DC9E00',
        'fillOpacity': 0.5,
        'weight': 0.5
    }
).add_to(map)

inner_area_layer = folium.GeoJson(
    buffer_150m,
    name='150m Zone', 
    style_function=lambda feature: {
        'color': '#FF0000',
        'fillOpacity': 0.3,
        'weight': 0.5
    }
).add_to(map)

folium.LayerControl().add_to(map)

map.save(r"C:\Users\tuann\github\esl_scripts\output\trap_map_2.html")