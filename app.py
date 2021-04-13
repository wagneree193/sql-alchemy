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
