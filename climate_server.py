# Import Dependencies
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy import func
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, jsonify

# Create an engine sqlite database
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# lists out tables
Base.classes.keys()

# Save a reference
measurements = Base.classes.measurements
stations = Base.classes.stations

# Create a database session object
session = Session(engine)

# Calculations
tobs_lastyear = session.query( measurements.date,func.avg(measurements.tobs)).filter(measurements.date.between('2016-08-24', '2017-08-23')).group_by(measurements.date).all()
tobs_lastyear_dict = dict(tobs_lastyear)

all_stations = session.query(measurements.station).group_by(measurements.station).order_by(func.count(measurements.station).desc()).all()
allstations = [station[0] for station in all_stations]

tobs_only = session.query(measurements.tobs).filter(measurements.date.between('2016-08-24', '2017-08-23')).all()
tobsonly = [tobs[0] for tobs in tobs_only]

app = Flask(__name__)

@app.route("/")
def index():
    return ("<br><strong>Welcome to the Climate App!</strong><br/>\
    <br><u>Available Routes:</u><br/>\
    <br/><body>/api/v1.0/precipitation<br/>   \
    /api/v1.0/stations<br/>     \
    /api/v1.0/tobs<br/> \
    /api/v1.0/&ltstart&gt<br/> \
    /api/v1.0/&ltstart&gt/&ltend&gt\
    </body>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(tobs_lastyear_dict)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(allstations)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(tobsonly)

@app.route("/api/v1.0/<start>")
def start_date(start):
    x = session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).\
    filter(measurements.date>=start).first()
    temp_summary = {"TMIN": x[0],
                   "TMAX": x[1],
                   "TAVG": x[2]}
    return jsonify(temp_summary)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    x = session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).\
    filter(measurements.date.between(start, end)).first()
    temp_summary = {"TMIN": x[0],
                "TMAX": x[1],
                "TAVG": x[2]}
    return jsonify(temp_summary)

if __name__ == "__main__":
    app.run(debug=True)

