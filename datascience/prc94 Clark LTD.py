import sys
import os
import pandas as pd
import sqlite3 as sq

# ==========================================================
# Base path (Windows)
# ==========================================================
BASE = r"C:\VKHCG"

print("==============================================")
print("Using WINDOWS base path:", BASE)
print("==============================================")

# ==========================================================
# Input CSV file (your real file)
# ==========================================================
INPUT_FILE = r"C:\Users\Medhansh\Downloads\Retrieve_DE_Billboard_Locations.csv"
print("Loading Billboard Data From:", INPUT_FILE)
print("==============================================")

# ==========================================================
# Load CSV
# ==========================================================
df = pd.read_csv(INPUT_FILE)

# Rename columns to clean format
df = df.rename(columns={
    "Place.Name": "Place_Name"
})

# Check required columns
required_cols = ["ID", "Country", "Place_Name", "Latitude", "Longitude"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    raise ValueError("Missing columns in CSV: " + ", ".join(missing))

# Fill missing values
df["Place_Name"] = df["Place_Name"].fillna("Unknown")

# ==========================================================
# Database setup
# ==========================================================
COMPANY = "01-Vermeulen"
DB_PATH = os.path.join(BASE, COMPANY, "06-Report", "SQLite")

# Ensure folder exists
os.makedirs(DB_PATH, exist_ok=True)

DB_NAME = os.path.join(DB_PATH, "billboards.db")

# Remove old DB if corrupted
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    print("Old database removed.")

# Create new DB connection
conn = sq.connect(DB_NAME)
print("New database created at:", DB_NAME)

# ==========================================================
# Store dataframe to database
# ==========================================================
df.to_sql("Billboards", conn, if_exists="replace", index=False)
print("Data stored in table 'Billboards'.")

# ==========================================================
# Verify table content
# ==========================================================
test = pd.read_sql_query("SELECT COUNT(*) AS Total FROM Billboards;", conn)
print("Total billboard rows loaded:", test["Total"].iloc[0])

conn.close()
print("==============================================")
print("PROCESS COMPLETE — All fixed and working!")
print("==============================================")
