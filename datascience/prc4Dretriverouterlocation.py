import os
import pandas as pd

# Input and output filenames
InputFileName = 'IP_DATA_CORE.csv'
OutputFileName = 'Retrieve_Router_Location.csv'

# Base folder where the CSV is located
Base = 'C:/Users/Medhansh/Downloads'

# Full path to input CSV
sFileName = os.path.join(Base, InputFileName)
print('Loading:', sFileName)

# Read CSV using exact column names
IP_DATA_ALL = pd.read_csv(
    sFileName,
    usecols=['Country', 'Place Name', 'Latitude', 'Longitude'],  # match CSV exactly
    encoding="latin-1"
)

# Rename column to a consistent format
IP_DATA_ALL.rename(columns={'Place Name': 'Place_Name'}, inplace=True)

# Output folder
sFileDir = os.path.join(Base, 'Router_Output')
os.makedirs(sFileDir, exist_ok=True)

# Drop duplicates
ROUTERLOC = IP_DATA_ALL.drop_duplicates()

print('Rows:', ROUTERLOC.shape[0])
print('Cols:', ROUTERLOC.shape[1])

# Save CSV
sFileName2 = os.path.join(sFileDir, OutputFileName)
ROUTERLOC.to_csv(sFileName2, index=False, encoding="latin-1")

print('### Done!! ############################################')
