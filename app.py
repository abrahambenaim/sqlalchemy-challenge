%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import extract
from sqlalchemy import and_
from sqlalchemy import or_
from mpl_toolkits.basemap import Basemap
from flask import jsonify

engine = create_engine("sqlite:////Users/cla/Desktop/UM Data Science/Homework/10 -sqlalchemy-challenge/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


app = Flask(__trip__)

@app.route('/')
def home():
    return 'Welcome to my homepage'

@app.route('/api/v1.0/precipitation')
def precipitation():
    query_date = input(f'Please enter a day to search for historic precipitation (yyy-mm-dd)')
    prcp = session.query(Measurement.date,Measurement.station,Measurement.prcp).filter(Measurement.date>=query_date).order_by(Measurement.date).all()
    prcp_df = pd.DataFrame(last_year).set_index('date').dropna()
    return jsonify(prcp_df)

@app.route('/api/v1.0/stations')
def stations()
    station_names = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    station_names = pd.DataFrame(station_names)
    return jsonify(station_names)

@app.route('/api/v1.0/tobs')
def tobs()
    last_date=session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()

    for date in last_date:
        split_last_date=date.split('-')
    
    last_year=int(split_last_date[0]); last_month=int(split_last_date[1]); last_day=int(split_last_date[2])

    query_date = dt.date(last_year, last_month, last_day) - dt.timedelta(days=365)

    last_year_tobs = session.query(Measurement.date,Measurement.station,Measurement.prcp).\
    filter(Measurement.date>=query_date).\
    order_by(Measurement.date).all()

    last_year_tobs_df = pd.DataFrame(last_year_tobs).set_index('date').dropna()
    return jsonify(last_year_tobs_df)

@app.route('/api/v1.0/<start>/<end>')
def start()
    dates = []
    start_date = input(f'Start date of your trip(yyyy-mm-dd)')
    end_date = input(f'End date of your trip(yyyy-mm-dd)') 

    for date in start_date, end_date:
        split_date=date.split('-')
        dates.append(split_date)
        
    start,end = dates

    start_year=(start[0]); start_month=(start[1]); start_day=(start[2])
    end_year=(end[0]); end_month=(end[1]); end_day=(end[2])

    trip = session.query(Measurement.date,func.avg(Measurement.tobs),\
    func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.prcp)).\
    filter(or_(and_(extract('day', Measurement.date)>=start_day,extract('month', Measurement.date)==start_month),\
    (and_(extract('day', Measurement.date)<=end_day,extract('month', Measurement.date)==end_month)))).\
    group_by(Measurement.date).all()


    trip_forecast_df = pd.DataFrame(trip, columns=['Date','Avg_Temp','Avg_Max_Temp','Avg_Min_Temp','Avg_Precipitation'])
    return jsonify(trip_forecast_df)

if __trip__ == "__main__":
    app.run(debug=True)
