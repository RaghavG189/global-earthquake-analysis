#import libraries
import pandas as pd
import sqlite3 as sq
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

#Sets up data files
DATA_FOLDER = 'data'
DB_FILE = 'earthquakes.db'
MODEL_FILE = 'model.pkl'

#Construct paths
DB_PATH = os.path.join(DATA_FOLDER, DB_FILE)
MODEL_PATH = os.path.join(DATA_FOLDER, MODEL_FILE)

#load data from database
print("Connecting to database...")
conn = sq.connect(DB_PATH) #Connect to database

retrieve_df_query = 'SELECT latitude, longitude, depth, mag FROM earthquakes;' #Query to retrieve all rows

print("Retrieving dataframe...")
loaded_earthquakes_df = pd.read_sql(retrieve_df_query, conn) #Run query to retrieve dataframe

conn.close() #Close the connection

#Define features and target variable
X = loaded_earthquakes_df[['latitude', 'longitude', 'depth']]
y = loaded_earthquakes_df['mag']

#Divide data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

#Create the randomforestregressor model
print("Creating ML model...")
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

#Train model on data
rf_model.fit(X_train, y_train)

#Store predicted values from test set
predictions = rf_model.predict(X_test)


#Save the .pkl file
print(f"Saving ML model at {MODEL_PATH}")
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(rf_model, f)

print("Model Created Successfully!")