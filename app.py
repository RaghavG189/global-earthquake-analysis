import streamlit as st
import pandas as pd
import sqlite3 as sq
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns

#Sets up data files
DATA_FOLDER = 'data'
DB_FILE = 'earthquakes.db'
MODEL_FILE = 'model.pkl'

#Construct paths
DB_PATH = os.path.join(DATA_FOLDER, DB_FILE)
MODEL_PATH = os.path.join(DATA_FOLDER, MODEL_FILE)

def load_data():
    conn = sq.connect(DB_PATH) #connect to database

    df = pd.read_sql('SELECT * FROM earthquakes', conn) #Retrieve df using query
    conn.close() #Close the connection

    return df #Return the dataframe

earthquakes_df = load_data() #Call function


@st.cache_resource #Caches model to speed repeated runs
def load_model():
    with open(MODEL_PATH, 'rb') as f: #Open ML model
        return pickle.load(f) #Return model
    
random_forest_model = load_model() #Call function

st.set_page_config(layout='wide') #Make page width wide

st.title('EARTHQUAKE: GLOBAL TRACKER')
st.write('An analysis of global earthquake data from USGS.')

#Metrics to display at top of the page
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric('Total Earthquakes: ', len(earthquakes_df))
metric_col2.metric('Max Magnitude Recorded: ', earthquakes_df['mag'].max())
metric_col3.metric('Time Period', 'Past 30 Days')

#Visualization of the map
st.subheader('Global Activity Map of Earthquakes')
st.map(earthquakes_df)


chart_col1, chart_col2 = st.columns(2) #Align both charts side by side
#Magnitude Frequency Chart
with chart_col1:
    st.subheader('Magnitude Frequency')
    fig, ax = plt.subplots() #Create image and specific graph
    sns.histplot(data=earthquakes_df, x='mag', bins=20, ax=ax, color="#ff0000") #Create histoplot

    ax.set_title('Distribution of Earthquake Magnitudes') 
    ax.set_ylabel('Frequency (count)')
    ax.set_xlabel('Magnitude')

    st.pyplot(fig) #Display histoplot using streamlit

with chart_col2:
    st.subheader('Correlation: Depth vs. Magnitude')
    fig2, ax = plt.subplots() #Create image and specific graph
    sns.scatterplot(data=earthquakes_df, x='mag', y='depth', ax=ax, hue='mag') #Create scatterplot

    ax.set_title('Depth vs. Magnitude')
    ax.set_ylabel('Depth')
    ax.set_xlabel('Magnitude')

    st.pyplot(fig2) #Display scatterplot using streamlit

#Create header for ML Model
st.header('Earthquake Magnitude Predictor')
st.write('Adjust various sliders to simulate an earthquake scenario.')

#Create sliders for features
latitude_input = st.slider('Pick value for latitude', -90, 90)
longitude_input = st.slider('Pick value for longitude', -180, 180)
depth_input = st.slider('Pick value for depth', 0, 700)

#Predict magnitude value given feature values
if st.button('Predict Magnitude'):
    user_input = [[latitude_input, longitude_input, depth_input]]

    prediction = random_forest_model.predict(user_input)

    predicted_magnitude = prediction[0]

    st.success(f'The predicted magnitude was: {predicted_magnitude:.2f}')