import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/Hawaii.sqlite", echo=False)
session = Session(engine)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
# tobs = Base.classes.tobs

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
        f"<center><h1>Welcome to the Home Page</h1><br/>"
        f"<h3>Available Routes:</h3><br/>"
        f"Precipitation     |     /api/v1.0/precipitation<br/>"
        f"Stations     |     /api/v1.0/stations<br/>"
        f"TOBS for Prevous Year     |     /api/v1.0/tobs<br/>"
        f"Start Temp Calculations (yyyy-mm-dd)     |     /api/v1.0/&lt;start&gt<br/>"
        f"Start to End Temp Calculations (yyyy-mm-dd)    |     /api/v1.0/&lt;start&gt/&lt;end&gt<br/></center>"
    )
#   * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

#   * Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB

    """Return a list of all passenger names"""
    # Precipitation Date
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date>'2016-08-22').order_by(measurement.date.desc()).all()

    session.close()
    
    # Create a dictionary from the row data and append to a list of all_dates
    all_dates = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] =  prcp
        # prcp_dict["prcp"] = prcp
        all_dates.append(prcp_dict)

    return jsonify(all_dates)


  # * Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB

#     """Return a list of all stations""
#     # Query all passengers
    results = session.query(station.name).all()

    session.close()

    # Return a JSON list of stations from the dataset
    all_names = list(np.ravel(results))

    return jsonify(all_names)

#   * Query the dates and temperature observations of the most active station for the last year of data.

#   * Return a JSON list of temperature observations (TOBS) for the previous year.

# @app.route("/api/v1.0/tobs")
# def tobs():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#  #Query the dates and temperature observations of the most active station for the last year of data.
#     results =session.query(measurement.date, measurement.tobs,measurement.station).filter(measurement.station=='USC00519281').filter(measurement.date>'2016-08-17').order_by(measurement.date.desc()).all()


#     session.close()

#     # list of temperature observations (TOBS) for the previous year
#     all_tobs = []
#     c = 0
#     for date,tobs,station in results:
#         # prcp_dict= {}
#         prcp_dict[c] =tobs
#         c=c+1
#     #     # prcp_dict["prcp"] = prcp
#         all_tobs.append(prcp_dict)

#     return jsonify(prcp_dict)

# if __name__ == '__main__':
#     app.run(debug=True)
@app.route("/api/v1.0/tobs")
def tobs():
    # """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query the primary station for all tobs from the last year
    results = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= prev_year).all()

    session.close()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))

    # Return the results
    return jsonify(temps=temps)


    
#     * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

# @app.route("/api/v1.0/<start>")
# def date(start=None):
    
#    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    
#     temp_query_start = session.query(func.min(measurement.tobs).label("TMIN"),func.max(measurement.tobs).label("TMAX"),\
#                     func.avg(measurement.tobs).label("TAVG")).filter(measurement.date ).all()


#     all_temp_query = []
    
#     for row in temp_query_start:
#         row_dict = {}
#         row_dict["minimum temperature"] = row.TMIN
#         row_dict["maximum temperature"] = row.TMAX
#         row_dict["average temperature"] = row.TAVG
#         all_temp_query.append(row_dict)
#     session.close()
#     return jsonify(all_temp_query)


# @app.route("/api/v1.0/<start>/<end>")
# def date_range(start,end):
    
#    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#     temp_query = session.query(func.min(measurement.tobs).label("TMIN"),func.max(measurement.tobs).label("TMAX"),\
#                     func.avg(measurement.tobs).label("TAVG")).filter(measurement.date>=start).filter(measurement.date<=end).all()
    
#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_temp_query = []
    
#     for row in temp_query:
#         row_dict = {}
#         row_dict["minimum temperature"] = row.TMIN
#         row_dict["maximum temperature"] = row.TMAX
#         row_dict["average temperature"] = row.TAVG
#         all_temp_query.append(row_dict)
#     session.close()
#     return jsonify(all_temp_query)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date(start=None,end=None):
    print(start)

    # start_dt=dt.datetime.strptime(start,'%d%m%Y')
    

    if not end: 
   # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
        
        temp_query = session.query(func.min(measurement.tobs).label("TMIN"),func.max(measurement.tobs).label("TMAX"),\
                        func.avg(measurement.tobs).label("TAVG")).filter(measurement.date>=start).all()
    else:
        # end_dt=dt.datetime.strptime(end,'%d%m%Y')
        temp_query = session.query(func.min(measurement.tobs).label("TMIN"),func.max(measurement.tobs).label("TMAX"),\
                    func.avg(measurement.tobs).label("TAVG")).filter(measurement.date>=start).filter(measurement.date<=end).all()

    all_temp_query = []
    
    for row in temp_query:
        row_dict = {}
        row_dict["minimum temperature"] = row.TMIN
        row_dict["maximum temperature"] = row.TMAX
        row_dict["average temperature"] = row.TAVG
        all_temp_query.append(row_dict)
    session.close()
    return jsonify(all_temp_query)

if __name__ == "__main__":
    app.run(debug=True)
