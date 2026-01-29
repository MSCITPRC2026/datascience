import sys
import os
import pandas as pd
from math import radians, cos, sin, asin, sqrt

################################################################
def haversine(lon1, lat1, lon2, lat2, stype):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 if stype == 'km' else 3956
    return round(c * r, 3)

################################################################
Base = 'C:/VKHCG'

sFileName = 'C:/Users/Medhansh/Downloads/IP_DATA_CORE.csv'
print('Loading:', sFileName)

# FIX: Load file without usecols
IP_DATA_ALL = pd.read_csv(
    sFileName,
    header=0,
    low_memory=False,
    encoding="latin-1"
)

print("Columns:", IP_DATA_ALL.columns.tolist())

# Try different possible column names
for col in IP_DATA_ALL.columns:
    if "Place" in col:
        place_col = col

################################################################
sFileDir = Base + '/01-Vermeulen/01-Retrieve/01-EDS/02-Python'
os.makedirs(sFileDir, exist_ok=True)

################################################################
IP_DATA = IP_DATA_ALL[['Country', place_col, 'Latitude', 'Longitude']].drop_duplicates()
IP_DATA.rename(columns={place_col: 'Place_Name'}, inplace=True)
IP_DATA.insert(0, 'K', 1)

################################################################
print(IP_DATA.shape)

################################################################
IP_CROSS = pd.merge(IP_DATA, IP_DATA, on='K')
IP_CROSS.drop('K', axis=1, inplace=True)

IP_CROSS.rename(columns={
    'Longitude_x': 'Longitude_from',
    'Longitude_y': 'Longitude_to',
    'Latitude_x': 'Latitude_from',
    'Latitude_y': 'Latitude_to',
    'Place_Name_x': 'Place_Name_from',
    'Place_Name_y': 'Place_Name_to',
    'Country_x': 'Country_from',
    'Country_y': 'Country_to'
}, inplace=True)

################################################################
IP_CROSS['DistanceBetweenKilometers'] = IP_CROSS.apply(
    lambda row: haversine(
        row['Longitude_from'], row['Latitude_from'],
        row['Longitude_to'], row['Latitude_to'], 'km'
    ), axis=1
)

IP_CROSS['DistanceBetweenMiles'] = IP_CROSS.apply(
    lambda row: haversine(
        row['Longitude_from'], row['Latitude_from'],
        row['Longitude_to'], row['Latitude_to'], 'miles'
    ), axis=1
)

################################################################
print(IP_CROSS.shape)

sFileName2 = sFileDir + '/Retrieve_IP_Routing.csv'
IP_CROSS.to_csv(sFileName2, index=False, encoding="latin-1")

print('### Done!! ############################################')
