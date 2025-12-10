#import libraries
import pandas as pd
import sqlite3 as sq
import os

#Sets up data files
DATA_FOLDER = 'data'
DB_FILE = 'earthquakes.db'
CSV_FILE = 'all_earthquakes_by_month.csv'

#Construct paths
DB_PATH = os.path.join(DATA_FOLDER, DB_FILE)
CSV_PATH = os.path.join(DATA_FOLDER, CSV_FILE)

#Create data folder if not present
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

#extracts contents from csv file
print(f"Reading CSV File {CSV_FILE}...")
try:
    earthquake_df = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    print("File was not found. Please make sure the CSV file is in the data folder.")
    exit()


print("Cleaning Data...")
#Drops unnecessary columns with 1000+ NaNs
columns_to_drop = earthquake_df[earthquake_df.columns.difference(['time', 'latitude', 'longitude', 'depth', 'mag', 'magType', 'place', 'type'])]
clean_earthquake_df = earthquake_df.drop(columns=columns_to_drop)

#Drops NaN rows for mag and magType
if set(['mag', 'magType']).issubset(clean_earthquake_df.columns):
    clean_earthquake_df.dropna(subset=['mag', 'magType'], inplace=True)

#Only keeps rows where type is 'earthquake'
types_to_drop = ['quarry blast', 'explosion', 'sonic boom', 'ice quake']
if 'type' in clean_earthquake_df.columns:
    clean_earthquake_df = clean_earthquake_df[~clean_earthquake_df['type'].isin(types_to_drop)]

#Creates a new column - region and inserts into dataframe
if 'place' in clean_earthquake_df.columns:
    clean_earthquake_df.insert(7, "region", clean_earthquake_df['place'].apply(lambda x: x.split()[-1]))

#Change CA to California for consistency
if 'region' in clean_earthquake_df.columns:
    clean_earthquake_df['region'] = clean_earthquake_df['region'].replace('CA', 'California')

print(f"Saving to database at {DB_FILE}")
#Creates and Connects to local SQLite file
conn = sq.connect(DB_PATH)

#Writes dataset to SQL table
clean_earthquake_df.to_sql('earthquakes', conn, if_exists='replace', index=False)

#Closes the connection
conn.close()

print("Database Created Successfully!")