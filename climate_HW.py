#!/usr/bin/env python
# coding: utf-8

# # Import Dependencies

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd


# In[3]:


import datetime as dt


# In[173]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import extract
from sqlalchemy import and_
from sqlalchemy import or_
from mpl_toolkits.basemap import Basemap


# In[174]:


from flask import jsonify


# # Reflect Tables into SQLAlchemy ORM

# In[5]:


engine = create_engine("sqlite:////Users/cla/Desktop/UM Data Science/Homework/10 -sqlalchemy-challenge/Resources/hawaii.sqlite")


# In[6]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[7]:


# We can view all of the classes that automap found
Base.classes.keys()


# In[8]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[9]:


# Create our session (link) from Python to the DB
session = Session(engine)


# # Exploratory Climate Analysis

# In[10]:


last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()

for date in last_date:
    split_last_date=date.split('-')
    
last_year=int(split_last_date[0]); last_month=int(split_last_date[1]); last_day=int(split_last_date[2])

query_date = dt.date(last_year, last_month, last_day) - dt.timedelta(days=365)

print(query_date)


# # Precipitation Analysis 

# In[11]:


last_year = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=query_date).order_by(Measurement.date).all()

last_year

last_year_df = pd.DataFrame(last_year).set_index('date').dropna()


# In[12]:


last_year_df.head()


# In[13]:


last_year_df.plot(figsize=(15,15))
plt.show()


# In[14]:


# Use Pandas to calcualte the summary statistics for the precipitation data

prcp_stats = last_year_df.describe()

prcp_stats


# # Station Analysis

# In[15]:


#Stations available in dataset

station_count = session.query(Measurement.station).group_by(Measurement.station).count()

station_count


# In[16]:


# The most active stations
station_activity = session.query(func.count(Measurement.station).label('count'), Measurement.station).group_by(Measurement.station).order_by('count').all()

station_activity_df = pd.DataFrame(station_activity).dropna()

station_activity_df = station_activity_df.sort_values(by='count', ascending=False)

station_activity_df


# In[141]:


station_names = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
station_names = pd.DataFrame(station_names)
station_names


# In[18]:


most_active = station_activity_df.head(1)
most_active_station = most_active['station'].values[0]
print('The most active station is: ' + str(most_active_station))


# In[19]:


least_active = station_activity_df.sort_values(by='count').head(1)
least_active_station = least_active['station'].values[0]
print('The least active station is: ' + str(least_active_station))


# In[20]:


# The lowest temperature recorded

station_temperature = session.query(func.min(Measurement.tobs).label('min_temp'), Measurement.station).group_by(Measurement.station).order_by('min_temp').all()

station_mintemp_df = pd.DataFrame(station_temperature).dropna()

station_mintemp_df = station_mintemp_df.sort_values(by='min_temp')

min_temp_recorded = station_mintemp_df['min_temp'].values[0]
min_temp_station = station_mintemp_df['station'].values[0]
print('The minimum temperature recorded is ' + str(min_temp_recorded) + ' in station ' + str(min_temp_station))

station_mintemp_df


# In[21]:


#Lowest and highest temperature recorded, and average temperature of the most active station

most_active_summary = session.query(func.count(Measurement.station).label('count'), Measurement.station,(func.max(Measurement.tobs)), (func.min(Measurement.tobs)), (func.avg(Measurement.tobs))).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()

most_active_summary


# In[22]:


#Temperatures recorded at the most active station in the last year
most_active_station

most_active_ly = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>=query_date).filter(Measurement.station==most_active_station).order_by(Measurement.date).all()

most_active_ly_df = pd.DataFrame(most_active_ly)
most_active_ly_df.plot.hist(bins=12)
plt.show()


# In[148]:


#Date weather calculator (search for weather in historical data)

start_date = input(f'Enter a date to search the weather(yyyy-mm-dd)')
end_date = input(f'End date of your search(yyyy-mm-dd)') 



def calc_temps(start_date, end_date):
    
    trip_temps = session.query(Measurement.date,func.avg(Measurement.tobs),func.max(Measurement.tobs),func.min(Measurement.tobs)).    group_by(Measurement.date).    filter(Measurement.date>=start_date, Measurement.date <= end_date).all()
    
    return(trip_temps)
calc_temps(start_date, end_date)


# In[149]:


x = calc_temps(start_date, end_date)

trip_temp_df = pd.DataFrame(x, columns=['Date','Avg_Temp','Max_Temp','Min_Temp'])

trip_temp_df.plot.bar()
plt.show()


# # Weather forecast calculator for your future trip

# In[160]:


#Enter your planned trip datess
dates = []
start_date = input(f'Start date of your trip(yyyy-mm-dd)')
end_date = input(f'End date of your trip(yyyy-mm-dd)') 

for date in start_date, end_date:
    split_date=date.split('-')
    dates.append(split_date)
    
start,end = dates

start_year=(start[0]); start_month=(start[1]); start_day=(start[2])
end_year=(end[0]); end_month=(end[1]); end_day=(end[2])


# In[161]:


#Trip weather calculator

trip = session.query(Measurement.date,func.avg(Measurement.tobs),func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.prcp)).filter(or_(and_(extract('day', Measurement.date)>=start_day,extract('month', Measurement.date)==start_month),(and_(extract('day', Measurement.date)<=end_day,extract('month', Measurement.date)==end_month)))).group_by(Measurement.date).all()


trip_forecast_df = pd.DataFrame(trip, columns=['Date','Avg_Temp','Avg_Max_Temp','Avg_Min_Temp','Avg_Precipitation'])
trip_forecast_df.head(5)


# In[162]:


#Forecast for planned trip

print(f'During your planned trip: From ' + (start_date)  + ' to: ' + (end_date) + ' the weather forecast is the following: ')
print(trip_avgforecast_df.mean())


# In[166]:


trip_forecast_summary


# In[172]:


fig,ax=plt.subplots()
for i in range(3):
    ax.bar(x=i,height=trip_forecast_summary[i])
ax2=ax.twinx()
ax2.bar(x=3,height=trip_forecast_summary[3])


# In[163]:


trip_forecast_summary = trip_avgforecast_df.mean()
trip_forecast_summary.plot.bar()


# In[147]:


# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
trip_rain = session.query(Measurement.station,func.avg(Measurement.prcp)).filter(or_(and_(extract('day', Measurement.date)>=start_day,extract('month', Measurement.date)==start_month),(and_(extract('day', Measurement.date)<=end_day,extract('month', Measurement.date)==end_month)))).group_by(Measurement.station).all()

trip_rain = pd.DataFrame(trip_rain, columns=['Station','Avg_Precipitation'])

trip_rain

trip_rain_df = trip_rain.merge(station_names, left_on='Station', right_on='station')
del trip_rain_df['station']
trip_rain_df = trip_rain_df.set_index('Station')

# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation

trip_rain_df.sort_values(by=['Avg_Precipitation'], ascending=False)


# ## Optional Challenge Assignment

# In[184]:


# Daily normals 

date_normal = input(f'Inser a month and a day to check historic weather behaviour(mm-dd)')

def daily_normals(date_normal):
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date_normal).all()
    
daily_normals(date_normal)