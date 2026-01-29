+ CompanyIn + '/00-RawData/' + InputFileName
print('Loading :', sFileName)

# Read CSV file
IP_DATA_ALL = pd.read_csv(sFileName, header=0, low_memory=False)
IP_DATA_ALL.rename(columns={'Place Name': 'Place_Name', 'First IP Number': 'First_IP_Number', 'Last IP Number': 'Last_IP_Number', 'Post Code': 'Post_Code'}, inplace=True)

################################################################
import sys
import os
import pandas as pd
import xml.etree.ElementTree as ET
################################################################

# Function to convert DataFrame to XML
def df2xml(data):
    header = data.columns
    root = ET.Element('root')
    for row in range(data.shape[0]):
        entry = ET.SubElement(root, 'entry')
        for index in range(data.shape[1]):
            schild = str(header[index])
            child = ET.SubElement(entry, schild)
            text_value = str(data[schild][row]) if pd.notna(data[schild][row]) else 'n/a'
            child.text = text_value
        entry.append(child)
    result = ET.tostring(root)
    return result

# Function to convert XML to DataFrame
def xml2df(xml_data):
    try:
        root = ET.XML(xml_data)
    except ET.ParseError as e:
        print(f"XML ParseError: {e}")
        return pd.DataFrame()
    all_records = []
    for i, child in enumerate(root):
        record = {}
        for subchild in child:
            record[subchild.tag] = subchild.text
        all_records.append(record)
    return pd.DataFrame(all_records)

################################################################
InputFileName = 'IP_DATA_ALL.csv'
OutputFileName = 'Retrieve_Online_Visitor.xml'
CompanyIn = '01-Vermeulen'
CompanyOut = '02-Krennwallner'
################################################################

# Set base directory based on OS
if sys.platform == 'linux':
    Base = os.path.expanduser('~') + '/VKHCG'
else:
    Base = 'C:/VKHCG'

################################################################
print('################################')
print('Working Base :', Base, ' using ', sys.platform)
print('################################')
################################################################

sFileName = Base + '/' 
# Ensure output directory exists
sFileDir = Base + '/' + CompanyOut + '/01-Retrieve/01-EDS/02-Python'
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

# Process data
visitordata = IP_DATA_ALL.head(10000)
print('Original Subset Data Frame')
print('Rows :', visitordata.shape[0])
print('Columns :', visitordata.shape[1])
print(visitordata)

# Convert DataFrame to XML and save
print('Export XML')
sXML = df2xml(visitordata)
sFileName = sFileDir + '/' + OutputFileName
with open(sFileName, 'wb') as file_out:
    file_out.write(sXML)
print('Store XML:', sFileName)

# Read XML back into DataFrame and remove duplicates
xml_data = open(sFileName).read()
unxmlrawdata = xml2df(xml_data)
print('Raw XML Data Frame')
print('Rows :', unxmlrawdata.shape[0])
print('Columns :', unxmlrawdata.shape[1])
print(unxmlrawdata)

unxmldata = unxmlrawdata.drop_duplicates()
print('Deduplicated XML Data Frame')
print('Rows :', unxmldata.shape[0])
print('Columns :', unxmldata.shape[1])
print(unxmldata)
#################################################################
#print('### Done!! ############################################')
#################################################################
