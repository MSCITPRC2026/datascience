import os
import sys
import pandas as pd
from geopy.distance import geodesic

################################################################
# Input and Output Files
InputFileName = 'GB_Postcode_Warehouse.csv'
OutputFileName = 'Retrieve_GB_Warehouse.csv'
Company = '03-Hillman'

Base = 'C:/VKHCG'
print('################################')
print('Working Base:', Base, 'using', sys.platform)
print('################################')

################################################################
# Directory Setup
sFileDir = os.path.join(Base, Company, '01-Retrieve/01-EDS/02-Python')
os.makedirs(sFileDir, exist_ok=True)

################################################################
# Load Data
sFileName = os.path.join(Base, Company, '00-RawData', InputFileName)
print('###########')
print('Loading:', sFileName)
Warehouse = pd.read_csv(sFileName, header=0, low_memory=False)

# Clean Data
WarehouseClean = Warehouse[Warehouse.latitude != 0]
WarehouseGood = WarehouseClean[WarehouseClean.longitude != 0]
WarehouseGood.drop_duplicates(subset='postcode', keep='first', inplace=True)
WarehouseGood.sort_values(by='postcode', ascending=True, inplace=True)

################################################################
# Save Cleaned Data
sFileName = os.path.join(sFileDir, OutputFileName)
WarehouseGood.to_csv(sFileName, index=False)

################################################################
# Process Route Information
WarehouseLoop = WarehouseGood.head(20)

for i in range(WarehouseLoop.shape[0]):
    print('Run:', i, ' =======>>>>>>>>>>', WarehouseLoop.iloc[i]['postcode'])

# Create a working copy of WarehouseGood for processing
WarehouseHold = WarehouseGood.head(10000).copy()

# Add Transaction Type
WarehouseHold.loc[:, 'Transaction'] = 'WH-to-WH'

# Example Route Name
OutputLoopName = f"Retrieve_Route_WH-{WarehouseLoop.iloc[0]['postcode']}_Route.csv"

# Add Seller and Buyer Information
WarehouseHold.loc[:, 'Seller'] = f"WH-{WarehouseLoop.iloc[0]['postcode']}"
WarehouseHold.loc[:, 'Seller_Latitude'] = WarehouseLoop.iloc[0]['latitude']
WarehouseHold.loc[:, 'Seller_Longitude'] = WarehouseLoop.iloc[0]['longitude']
WarehouseHold.loc[:, 'Buyer'] = WarehouseHold['postcode'].apply(lambda x: f"WH-{x}")
WarehouseHold.loc[:, 'Buyer_Latitude'] = WarehouseHold['latitude']
WarehouseHold.loc[:, 'Buyer_Longitude'] = WarehouseHold['longitude']

# Calculate Distances
WarehouseHold.loc[:, 'Distance'] = WarehouseHold.apply(
    lambda row: round(
        geodesic(
            (WarehouseLoop.iloc[0]['latitude'], WarehouseLoop.iloc[0]['longitude']),
            (row['latitude'], row['longitude'])
        ).miles, 6),
    axis=1
)

# Drop Unnecessary Columns
WarehouseHold.drop(['id', 'postcode', 'latitude', 'longitude'], axis=1, inplace=True)

################################################################
# Save Processed Data
sFileLoopName = os.path.join(sFileDir, OutputLoopName)
WarehouseHold.to_csv(sFileLoopName, index=False)
################################################################
print('### Done!! ############################################')

