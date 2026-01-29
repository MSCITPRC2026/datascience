################################################################
# -*- coding: utf-8 -*-
################################################################
import sys
import os
import pandas as pd
from folium.plugins import FastMarkerCluster, HeatMap
from folium import Marker, Map
import webbrowser
################################################################

# Detect Base Path
if sys.platform == 'linux': 
    Base = os.path.expanduser('~') + '/VKHCG'
else:
    Base = 'C:/VKHCG'

print("################################")
print("Working Base :", Base, " using ", sys.platform)
print("################################")

################################################################
# INPUT FILE
################################################################

sInputFile = os.path.join(
    Base,
    '02-Krennwallner/01-Retrieve/01-EDS/02-Python/Retrieve_DE_Billboard_Locations.csv'
)

print("Loading:", sInputFile)
df = pd.read_csv(sInputFile, header=0, low_memory=False, encoding="latin-1")
df.fillna(value=0, inplace=True)

print("Loaded rows/cols:", df.shape)

################################################################
# CLEAN + PREPARE DATA
################################################################

DataCluster = []
DataPoint = []

for i in range(df.shape[0]):
    try:
        lat = float(df["Latitude"][i])
    except:
        lat = 0.0

    try:
        lon = float(df["Longitude"][i])
    except:
        lon = 0.0

    try:
        desc = str(df["Place_Name"][i]) + " (" + str(df["Country"][i]) + ")"
    except:
        desc = "VKHCG"

    if lat != 0.0 and lon != 0.0:
        DataCluster.append([lat, lon])
        DataPoint.append([lat, lon, desc])

pins = pd.DataFrame(DataPoint, columns=["Latitude", "Longitude", "Description"])

################################################################
# 1. FAST MARKER CLUSTER MAP
################################################################

stops_map1 = Map(location=[48.1459806, 11.4985484], zoom_start=5)
FastMarkerCluster(DataCluster).add_to(stops_map1)

output_html1 = os.path.join(Base, "02-Krennwallner/06-Report/01-EDS/02-Python/Billboard_cluster.html")
os.makedirs(os.path.dirname(output_html1), exist_ok=True)

stops_map1.save(output_html1)
webbrowser.open('file://' + os.path.realpath(output_html1))

################################################################
# 2. NORMAL MARKER MAP (first 100 points)
################################################################

stops_map2 = Map(location=[48.1459806, 11.4985484], zoom_start=5)

for _, row in pins.iloc[:100].iterrows():
    Marker([row["Latitude"], row["Longitude"]], popup=row["Description"]).add_to(stops_map2)

output_html2 = os.path.join(Base, "02-Krennwallner/06-Report/01-EDS/02-Python/Billboard2.html")
stops_map2.save(output_html2)
webbrowser.open('file://' + os.path.realpath(output_html2))

################################################################
# 3. HEATMAP
################################################################

stops_heatmap = Map(location=[48.1459806, 11.4985484], zoom_start=5)

heat_data = [[row["Latitude"], row["Longitude"]] for _, row in pins.iloc[:100].iterrows()]
stops_heatmap.add_child(HeatMap(heat_data))

output_html3 = os.path.join(Base, "02-Krennwallner/06-Report/01-EDS/02-Python/Billboard_heatmap.html")
stops_heatmap.save(output_html3)
webbrowser.open('file://' + os.path.realpath(output_html3))

################################################################
print("### Done!! ############################################")
################################################################
