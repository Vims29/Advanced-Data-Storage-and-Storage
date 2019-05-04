import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import pandas as pd 
import time
##################################################
# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")
##################################################
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
##################################################
# Flask Setup
##################################################
app = Flask(__name__)

##################################################
@app.route("/")
def welcome():

    """List all available api routes."""
    return (
        f"Hawaii weather!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"   
        f"/api/v1.0/start-date/YYYY-MM-DD<br/>"
        f"/api/v1.0/start-date/YYYY-MM-DD/end-date/YYYY-MM-DD<br/>"
    )
##################################################
@app.route("/api/v1.0/precipitation")
def precipitation():

    meas_one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    ppt_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= meas_one_year_ago).\
    order_by(Measurement.date).all()

    # Convert list of tuples into normal list
    all_precipitation = []
    for precipitation in ppt_data:
        precipitation_dict = {}
        precipitation_dict["date"] = precipitation.date
        precipitation_dict["prcp"] = precipitation.prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)
###################################################

@app.route("/api/v1.0/stations")
def stations():

    all_stations = session.query(Station.name,Station.station).all()

    statns = []
    for stations in all_stations:
        station_id = {"Name":stations[0], "Station": stations[1]}
        statns.append(stations)
    return jsonify(statns)
######################################################

@app.route("/api/v1.0/tobs")
def tobs():
    
    meas_one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    tobs_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= meas_one_year_ago).\
    order_by(Measurement.date).all()

    all_tobs = []
    for tob in tobs_data:
        temp = {"Date":tob[0], "Temp": tob[1]}
        all_tobs.append(temp)

    return jsonify(all_tobs)
#######################################################
@app.route("/api/v1.0/start-date/<start>")
def temp(start): 

    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.commit()

    return jsonify(temp_results)
#######################################################

@app.route("/api/v1.0/start-date/<start>/end-date/<end>")
def start_end(start, end):

    temp2_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
       filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.commit() 

    return jsonify(temp2_results) 
########################################################

if __name__ == '__main__':
    app.run(debug=True)
