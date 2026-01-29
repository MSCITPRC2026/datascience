import sqlite3 as sq
import pandas as pd
import os

################################################################
Base = 'C:/VKHCG'
sDatabaseDir = os.path.join(Base, '01-Vermeulen/00-RawData/SQLite')
sDatabaseName = os.path.join(sDatabaseDir, 'vermeulen.db')

# Ensure the directory exists
if not os.path.exists(sDatabaseDir):
    os.makedirs(sDatabaseDir)

# Connect to the SQLite database
conn = sq.connect(sDatabaseName)

################################################################
sFileName = os.path.join(Base, '01-Vermeulen/01-Retrieve/01-EDS/02-Python/Retrieve_IP_DATA.csv')
print('Loading :', sFileName)
IP_DATA_ALL_FIX = pd.read_csv(sFileName, header=0, low_memory=False)
IP_DATA_ALL_FIX.index.names = ['RowIDCSV']

# Save to SQLite
sTable = 'IP_DATA_ALL'
print('Storing :', sDatabaseName, ' Table:', sTable)
IP_DATA_ALL_FIX.to_sql(sTable, conn, if_exists="replace")

# Load from SQLite
print('Loading :', sDatabaseName, ' Table:', sTable)
TestData = pd.read_sql_query("SELECT * FROM IP_DATA_ALL;", conn)

# Display data
print('################')
print('## Data Values')
print('################')
print(TestData)

print('################')
print('## Data Profile')
print('################')
print('Rows :', TestData.shape[0])
print('Columns :', TestData.shape[1])

print('### Done!! ############################################')
