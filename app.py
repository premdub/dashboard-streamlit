import streamlit as st
import pandas as pd
import numpy as np
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import seaborn as sb
from pandas.api.types import CategoricalDtype
import inline
import inline
import splot
import containers
import seaborn as sns
import pydeck as pdk
import matplotlib.pyplot as plt

st.title('Bay Wheels trip data')


DATE_COLUMN = 'date/time'
DATA_URL = ('dataset/Bay_Wheels_trip_data_for_public_use2020.csv')


#@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")
st.subheader('DATASET #1:  Ford-go-Bike Trip Data')
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of bike pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)


code = '''st.subheader('Number of bike pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)'''
st.code(code, language='python')


# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)

code = '''st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)'''
st.code(code, language='python')


#-----------------------------------------------------------------------------------
st.title('US_Accidents_Dec21')
st.subheader('DATASET #2: US_Accidents_Dec21')

DATE_COLUMN_ = 'date/time'
DATA_URL_ = ('dataset/US_Accidents_Dec21.csv')
#@st.cache
def load_data(nrows):
    dataa = pd.read_csv(DATA_URL_, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    dataa.rename(lowercase, axis='columns', inplace=True)
    dataa[DATE_COLUMN_] = pd.to_datetime(dataa[DATE_COLUMN_])
    return dataa


data_load_state = st.text('Loading data...')
dataa = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data_'):
    st.subheader('Raw data_')
    st.write(dataa)

st.subheader('US States -Ranked by Population 2022')
st.subheader('Map of all States: Car Accidents Countrywide')
st.map(filtered_data)

code = '''st.subheader('US States -Ranked by Population 2022')
st.subheader('Map of all States:Car accidents countrywide')
st.map(filtered_data)'''
st.code(code, language='python')

#------------------------------------------------
#import pydeck as pdk
st.subheader('Car Accidents Countrywide, Within the USA')
df = pd.DataFrame(
   np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
   columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))

code = '''st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))'''
st.code(code, language='python')

#---------------------------
DATA_URL = ('dataset/US_Accidents_Dec21.csv')
dataa = pd.read_csv(DATA_URL)
data_clean = dataa.copy()
# changing strings to datetime and int to strings
data_clean['Start_Time'] = pd.to_datetime(data_clean['Start_Time'])
data_clean['End_Time'] = pd.to_datetime(data_clean['End_Time'])
data_clean['Weather_Timestamp'] = pd.to_datetime(data_clean['Weather_Timestamp'])

# let's get the start time in terms of day,hour and date
start_year = data_clean['Start_Time'].dt.strftime('%Y') # extracting year from date
start_hour = data_clean['Start_Time'].dt.strftime('%H') # extracting hour from date
start_day = data_clean['Start_Time'].dt.strftime('%A') # extracting day from date
start_month = data_clean['Start_Time'].dt.strftime('%b') # extracting month from date

#define the hour of the day with most accidents cases
dataa = pd.DataFrame(start_hour.sort_values())
dataa['ID'] = 1
hour = dataa[['Start_Time','ID']].groupby('Start_Time').count().reset_index()
hour['cases'] = ((hour['ID']/len(data_clean['ID']))*100).apply(lambda x: '{0:.2f}%'.format(x))

#Plot to explore the hour of the day with most accidents cases
fig, ax = plt.subplots(figsize=(16,5))
ax.spines['top'].set_visible(False) # removing the top spine of the border
ax.spines['right'].set_visible(False) # removing the right spine of the border
splot = sb.barplot(data = hour,x='Start_Time',y='ID',color=sb.color_palette()[0])
plt.bar_label(splot.containers[0],labels=hour['cases'],fontsize=15);
plt.xlabel('Hour of the day',fontsize=20)
plt.ylabel('Count',fontsize=20)
plt.title('Count of acidents per hour',fontsize=29);

st.pyplot(fig)


code = '''fig, ax = plt.subplots(figsize=(16,5))
ax.spines['top'].set_visible(False) # removing the top spine of the border
ax.spines['right'].set_visible(False) # removing the right spine of the border
splot = sb.barplot(data = hour,x='Start_Time',y='ID',color=sb.color_palette()[0])
plt.bar_label(splot.containers[0],labels=hour['cases'],fontsize=15);
plt.xlabel('Hour of the day',fontsize=20)
plt.ylabel('Count',fontsize=20)
plt.title('Count of acidents per hour',fontsize=29);

st.pyplot(fig)'''
st.code(code, language='python')