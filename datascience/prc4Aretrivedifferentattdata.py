import sys
import os
import pandas as pd

################################################################
# Use your Downloads folder because that's where your file is
sFileName = 'C:/Users/Medhansh/Downloads/IP_DATA_ALL.csv'
print('Loading :', sFileName)

IP_DATA_ALL = pd.read_csv(
    sFileName,
    header=0,
    low_memory=False,
    encoding="latin-1"
)
################################################################

# Output directory inside VKHCG (this part is fine)
Base = 'C:/VKHCG'
sFileDir = Base + '/01-Vermeulen/01-Retrieve/01-EDS/02-Python'
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

print('Rows:', IP_DATA_ALL.shape[0])
print('Columns:', IP_DATA_ALL.shape[1])
print('### Raw Data Set #####################################')

for col in IP_DATA_ALL.columns:
    print(col, type(col))

print('### Fixed Data Set ###################################')

IP_DATA_ALL_FIX = IP_DATA_ALL.copy()
for i in range(len(IP_DATA_ALL_FIX.columns)):
    old = IP_DATA_ALL_FIX.columns[i]
    new = old.strip().replace(" ", ".")
    IP_DATA_ALL_FIX.columns.values[i] = new
    print(new)

################################################################
print('Fixed Data Set with ID')
IP_DATA_ALL_FIX.index.names = ['RowID']

sFileName2 = sFileDir + '/Retrieve_IP_DATA.csv'
IP_DATA_ALL_FIX.to_csv(sFileName2, index=True, encoding="latin-1")

################################################################
print('### Done!! ############################################')
