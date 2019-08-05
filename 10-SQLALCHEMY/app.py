import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
from datetime import datetime
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/<start_date><br/>"
        f"/api/v1.0/start_date1/<start_date1>/end_date1/<end_date1><br/>"
        f"<br/>"
        f"IMP: Enter dates in YYYY-MM-DD format without any quotation marks<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Query
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    
    # Query to find list of stations
    session = Session(engine)

    results = session.query(Station.name).group_by(Station.name).all()

    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    
    # Query for the dates and temperature observations from a year from the last data point for station with highest number of tobs
    session = Session(engine)

    most_temp_obs = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).first()
    most_temp_obs_station = most_temp_obs[0]
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    observations = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_temp_obs_station).filter(Measurement.date >= year_ago).all()
    
    temp_data = []
    for date, temp in observations:
        temp_dict = {}
        temp_dict[date] = temp
        
        temp_data.append(temp_dict)


    return jsonify(temp_data)


@app.route("/api/v1.0/start_date/<start_date>")
def get_obs(start_date):
    
    # Query to calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date
    session = Session(engine)
    start_date_str = datetime.strptime(start_date, '%Y-%m-%d',)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date_str).all()
    
    temp_data = []
    for tmin, tavg, tmax in results:
        temp_dict = {}
        temp_dict['min temp'] = tmin
        temp_dict['avg temp'] = tavg
        temp_dict['max temp'] = tmax

        temp_data.append(temp_dict)

    return jsonify(temp_data)


@app.route("/api/v1.0/start_date1/<start_date1>/end_date1/<end_date1>")
def get_obs1(start_date1, end_date1):
    
    # Query to find minimum, maximum, and average temps for travel dates based on temperatures from 2016-8-23 to 2017-8-23
    session = Session(engine)
    year_ago_1 = datetime.strptime('2016-8-23', '%Y-%m-%d')
    start_date_val = datetime.strptime(start_date1, '%Y-%m-%d')
    end_date_val = datetime.strptime(end_date1, '%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= year_ago_1).filter(func.strftime('%m-%d', Measurement.date) >= func.strftime('%m-%d', start_date_val)).filter(func.strftime('%m-%d', Measurement.date) <= func.strftime('%m-%d', end_date_val)).all()

    temp_data_1 = []
    for tmin, tavg, tmax in results:
        temp_dict_1 = {}
        temp_dict_1['min temp'] = tmin
        temp_dict_1['avg temp'] = tavg
        temp_dict_1['max temp'] = tmax

        temp_data_1.append(temp_dict_1)

    return jsonify(temp_data_1)

if __name__ == '__main__':
    app.run(debug=True)
