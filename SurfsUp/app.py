# Import the dependencies.
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """Homepage"""
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a dictionary."""

    # Starting from the most recent data point in the database. 
    most_recent_date = dt.date(2017, 8, 23)
    # Calculate the date one year from the last date in data set.
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_data = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= one_year_ago).\
    filter(measurement.date <= most_recent_date).all()

    # Create a dictionary from the row data and append to a list
    prcp_list = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""

    # Query all stations
    station_results = session.query(station.station).all()

    # Convert list of tuples into normal list
    stations = list(np.ravel(station_results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Query temperature observations for the most active station for the previous year."""
    # Query to find the most active station
    most_active_station = session.query(measurement.station, func.count(measurement.station)).\
    group_by(measurement.station).\
    order_by(func.count(measurement.station).desc()).first()

    most_active_station_id = most_active_station[0]

    # Starting from the most recent data point in the database. 
    most_recent_date = dt.date(2017, 8, 23)
    # Calculate the date one year from the last date in data set.
    one_year_ago = most_recent_date - dt.timedelta(days=365)
    
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    temperature_data = session.query(measurement.tobs).\
    filter(measurement.station == most_active_station_id).\
    filter(measurement.date >= one_year_ago).\
    filter(measurement.date <= most_recent_date).all()

    # Convert the query results to a list of temperatures
    temperatures = [temp[0] for temp in temperature_data]

    return jsonify(temperatures)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return TMIN, TAVG, and TMAX for dates greater than or equal to the start date."""
    temp_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                   filter(measurement.date >= start).all()
    
    temps = {"TMIN": temp_results[0][0], "TAVG": temp_results[0][1], "TMAX": temp_results[0][2]}
    
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return TMIN, TAVG, and TMAX for dates between the start and end dates."""
    temp_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                   filter(measurement.date >= start).\
                   filter(measurement.date <= end).all()
    
    temps = {"TMIN": temp_results[0][0], "TAVG": temp_results[0][1], "TMAX": temp_results[0][2]}
    
    return jsonify(temps)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)