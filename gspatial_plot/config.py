import geopandas as gpd
import os

dir = os.path.dirname(os.path.abspath(__file__))
colors = [
    "#f77779",
    "#b6d86c",
    "#fccd7b",
    "#fb9677",
    "#fd453f",
    "#646e78",
    "#8d98a7",
    "#dcccbb",
    "#eab464",
    "#a7754d",
    "#fa8334",
    "#fffd77",
    "#ffe887",
    "#388697",
    "#776533",
    "#b47eb3",
    "#fdf5bf",
    "#ffd5ff",
    "#97d6c3",
    "#8bb8a8",
    "#4599f7",
    "#f4f4e7",
    "#eb9baf",
    "#f9e8ab",
    "#fbc5ae",
    "#668bc3",
    "#df5d68",
    "#f5cbcb",
    "#5fb6c4",
    "#c7ffe9",
    "#a54657",
    "#587635",
    "#f7ee7f",
    "#f6a66a",
    "#f76657",
    "#fbc7b5",
    "#ffa8a9",
    "#f786aa",
    "#a64a76",
    "#cdb7ab",
]
countries = gpd.read_file(os.path.join(dir, "datasets","ne_50m_admin_0_countries.shp"))
ocean = gpd.read_file(os.path.join(dir, "datasets","ne_50m_ocean.shp"))
gridlines = gpd.read_file(os.path.join(dir, "datasets","ne_50m_geographic_lines.shp"))
rivers = gpd.read_file(os.path.join(dir, "datasets","ne_50m_rivers_lake_centerlines.shp"))
lakes = gpd.read_file(os.path.join(dir, "datasets","ne_50m_lakes.shp"))
us_states = gpd.read_file(os.path.join(dir, "datasets","us_states.geojson"))