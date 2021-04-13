import numpy as np
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import warnings
#warnings.filterwarnings('ignore')

# Set up database
engine = create_engine("sqlite:///Resources/hawaii_2.sqlite")
# reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)
#save the reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


#Flask setup

app = Flask (__name__)

#make list of all available routes

@app.route ("/")
def welcome():
    """Available API Routes:"""
    return(
        f"Available routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"One Yr Temp: /api/v1.0/tobs<br/>"
        f"Temp Start Date Only: /api/v1.0/<start><br/>"
        f"Temp Start and End Date: /api/v1.0/<start>/<end><br/>"

    )

# convert precipitation query results into a dictionary using date as key and prcp as value
#return JSON representation of the dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    #create an empty list in which to append a list of dictionaries from the row data 
    prcp_list = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp.dict)

    return jsonify(prcp_dict)


#Return JSON list from the stations dataset
@app.route("/api/v1.0/stations")
def station ():
    session = Session(engine)
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify (all_stations)

#query dates and temp observations of most active station for last year of data
#return JSON list of tobs for previous year
@app.route("/api/v1.0/tobs")
def tobs ():
    session = Session (engine)
    final_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_ya = dt.datetime.strptime(final_date[0], '%Y-%m-%d')- dt.timedelta(days=365).strftime('%Y-%m-%d')
    station_activity = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).first()
    sel= [Measurement.date, Measurement.tobs]
    results = session.query(*sel).filter(Measurement.date>=one_ya).filter(Measurement.station == station_activity).all()

    session.close()
    year_tobs = list(np.ravel(results))
    return jsonify (year_tobs)


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def start (start):
    session = Session (engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    start_tobs = list(np.ravel(results))
    return jsonify (start_tobs)
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def range(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    tobs_range = list(np.ravel(results))
    return jsonify (tobs_range)