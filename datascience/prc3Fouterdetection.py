import pandas as pd

InputFileName = 'IP_DATA_CORE.csv'
OutputFileName = 'Retrieve_Router_Location.csv'

# Base directory (NOT a file!)
Base = 'C:/Users/Medhansh/Downloads'

print('################################')
print('Working Base :', Base)
print('################################')

# Correct full file path
sFileName = Base + '/' + InputFileName
print('Loading :', sFileName)

# Load CSV
IP_DATA_ALL = pd.read_csv(
    sFileName,
    header=0,
    low_memory=False,
    usecols=['Country', 'Place Name', 'Latitude', 'Longitude'],
    encoding="latin-1"
)

# Fix column name
IP_DATA_ALL.rename(columns={'Place Name': 'Place_Name'}, inplace=True)

# Filter for London
LondonData = IP_DATA_ALL.loc[IP_DATA_ALL['Place_Name'] == 'London']

# Select columns
AllData = LondonData[['Country', 'Place_Name', 'Latitude']]
print('All Data')
print(AllData)

# Mean and Std Dev
MeanData = AllData['Latitude'].mean()
StdData = AllData['Latitude'].std()

UpperBound = MeanData + StdData
LowerBound = MeanData - StdData

print('Outliers')
print('Higher than ', UpperBound)
OutliersHigher = AllData[AllData.Latitude > UpperBound]
print(OutliersHigher)

print('Lower than ', LowerBound)
OutliersLower = AllData[AllData.Latitude < LowerBound]
print(OutliersLower)

print('Not Outliers')
OutliersNot = AllData[(AllData.Latitude >= LowerBound) &
                      (AllData.Latitude <= UpperBound)]
print(OutliersNot)
