import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

app = Flask(__weather__)

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
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data based on date"""
    # Query date, prcp
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).all()

    session.close()

    # create dictionary 
    previous_year_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        previous_year_prcp.append(prcp_dict)

    return jsonify(previous_year_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations from the dataset"""
    # Query all stations
    station_results = session.query(Measurement.station).all()

    session.close()

    return jsonify(station_results)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list temperature observations by date for the previous year"""
    # Query dates and TOBS for the past year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= previous_year, Measurement.station == 'USC00519281').all()

    session.close()

    # Create a dictionary
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature observation"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return minimum, maximum, and average temperature for dates greater than or equal to start date"""
    # Query min, max, avg temp for dates after the start date
        min_results = session.query(func.min(Measurement.tobs).filter(Measurement.date >= <start>)).first()
        max_results = session.query(func.max(Measurement.tobs).filter(Measurement.date >= <start>)).first()
        avg_results = session.query(func.avg(Measurement.tobs).filter(Measurement.date >= <start>)).first()
    session.close()

    return '{} {} {}'.format(min_results, max_results, avg_results)

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return minimum, maximum, and average temperatures for dates between start and end"""
    # Query dates and TOBS for the past year
        min_results = session.query(func.min(Measurement.tobs).filter(<end> >= Measurement.date >= <start>)).all()
        max_results = session.query(func.max(Measurement.tobs).filter(<end> >= Measurement.date >= <start>)).all()
        avg_results = session.query(func.avg(Measurement.tobs).filter(<end> >= Measurement.date >= <start>)).all()
    session.close()

    return '{} {} {}'.format(min_results, max_results, avg_results)


if __name__ == '__main__':
    app.run(debug=True)
