# ##################################################
import sys
import os
import pandas as pd
################################################################
Base = 'C:/VKHCG'
################################################################

# Your actual CSV file path (ONLY use the real path)
sFileName = 'C:/Users/Medhansh/Downloads/IP_DATA_ALL.csv'
print('Loading :', sFileName)

IP_DATA_ALL = pd.read_csv(
    sFileName,
    header=0,
    low_memory=False,
    encoding="latin-1"
)
################################################################

sFileDir = Base + '/01-Vermeulen/01-Retrieve/01-EDS/02-Python'

if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

print('Rows:', IP_DATA_ALL.shape[0])
print('Columns:', IP_DATA_ALL.shape[1])
print('### Raw Data Set #####################################')

for i in range(len(IP_DATA_ALL.columns)):
    print(IP_DATA_ALL.columns[i], type(IP_DATA_ALL.columns[i]))

print('### Fixed Data Set ###################################')

IP_DATA_ALL_FIX = IP_DATA_ALL.copy()

for i in range(len(IP_DATA_ALL_FIX.columns)):
    old_col = IP_DATA_ALL_FIX.columns[i]
    new_col = old_col.strip().replace(" ", ".")
    IP_DATA_ALL_FIX.columns.values[i] = new_col
    print(new_col)

################################################################
print('Fixed Data Set with ID')

IP_DATA_ALL_FIX.index.names = ['RowID']

sFileName2 = sFileDir + '/Retrieve_IP_DATA.csv'
IP_DATA_ALL_FIX.to_csv(sFileName2, index=True, encoding="latin-1")

################################################################
print('### Done!! ############################################')
################################################################
