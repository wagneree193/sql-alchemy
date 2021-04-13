import numpy as numpy
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

#query dates and temp observations of most active station for last year of data
#return JSON list of tobs for previous year

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.