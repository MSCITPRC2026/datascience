import pandas as pd
import sys

InputFileName = 'IP_DATA_CORE.csv'
OutputFileName = 'Retrieve_Router_Location.csv'

# Folder where the file actually is
Base = 'C:/Users/Medhansh/Downloads'

print('################################')
print('Working Base :', Base, ' using ', sys.platform)
print('################################')

# Correct file path
sFileName = Base + '/' + InputFileName
print('Loading :', sFileName)

# Read CSV file
IP_DATA_ALL = pd.read_csv(
    sFileName, 
    header=0, 
    low_memory=False,
    usecols=['Country', 'Place Name', 'Latitude', 'Longitude'],
    encoding="latin-1"
)

# Rename column
IP_DATA_ALL.rename(columns={'Place Name': 'Place_Name'}, inplace=True)

# Select columns
AllData = IP_DATA_ALL[['Country', 'Place_Name', 'Latitude']]
print(AllData)

# Mean latitude
MeanData = AllData.groupby(['Country', 'Place_Name'])['Latitude'].mean()
print(MeanData)
