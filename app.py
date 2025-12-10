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
    fig, ax1 = plt.subplots() #Create image and specific graph
    sns.histplot(data=earthquakes_df, x='mag', bins=20, ax=ax1, color="#ff0000") #Create histoplot

    ax1.set_title('Distribution of Earthquake Magnitudes') 
    ax1.set_ylabel('Frequency (count)')
    ax1.set_xlabel('Magnitude')

    st.pyplot(fig) #Display histoplot using streamlit

#Correlation: Depth vs. Magnitude Chart
with chart_col2:
    st.subheader('Correlation: Depth vs. Magnitude')
    fig2, ax2 = plt.subplots() #Create image and specific graph
    sns.scatterplot(data=earthquakes_df, x='mag', y='depth', ax=ax2, hue='mag') #Create scatterplot

    ax2.set_title('Depth vs. Magnitude')
    ax2.set_ylabel('Depth')
    ax2.set_xlabel('Magnitude')

    st.pyplot(fig2) #Display scatterplot using streamlit


chart_col3, chart_col4 = st.columns(2)#Align charts side by side
#Earthquakes by Region Chart
with chart_col3:
    st.subheader('Top Earthquake Regions')
    fig3, ax3 = plt.subplots() #Create image and specific graph
    
    top_regions_ten = earthquakes_df['region'].value_counts().head(10).index #Get top 10 regions
    region_ten = earthquakes_df[earthquakes_df['region'].isin(top_regions_ten)] #Get dataframe with top regions

    sns.countplot(data=region_ten, y='region', order=top_regions_ten, ax=ax3, palette='magma') #Create countplot

    ax3.set_title('Top 10 Regions by Quake Count')
    ax3.set_ylabel('Region')
    ax3.set_xlabel('Number of Earthquakes')

    st.pyplot(fig3) #Display countplot using streamlit

#Magnitude Intensity by Region Chart
with chart_col4:
    st.subheader('Magnitude Intensity by Region Chart')
    fig4, ax4 = plt.subplots() #Create image and specific graph

    top_regions_five = earthquakes_df['region'].value_counts().head(5).index #Get top 5 regions
    region_five = earthquakes_df[earthquakes_df['region'].isin(top_regions_five)] #Get dataframe with top regions
    
    sns.boxplot(data=region_five, x='region', y ='mag', ax=ax4, palette='Reds') #Create boxplot

    ax4.set_title('Intensity Comparison of Top 5 Regions')
    ax4.set_ylabel('Magnitude')
    ax4.set_xlabel('Region')

    st.pyplot(fig4) #Display boxplot using streamlit


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