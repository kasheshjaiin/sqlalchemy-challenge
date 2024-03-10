# Climate Analysis and Flask API

This project involves climate analysis and the development of a Flask API for accessing climate data from the Hawaii database.

## Climate Analysis

In the climate analysis part of the project, we utilized Python and SQLAlchemy to conduct basic climate analysis and data exploration of the climate database. We used SQLAlchemy ORM queries, Pandas, and Matplotlib to perform various analyses on the dataset.

### Steps involved in the analysis:

1. **Set up SQLAlchemy:** Connected to the SQLite database using the `create_engine()` function.

2. **Reflect the database:** Used the `automap_base()` function to reflect the tables into classes and saved references to the classes.

3. **Create a session:** Linked Python to the database by creating a SQLAlchemy session.

4. **Performed analyses:** Conducted precipitation analysis and station analysis to gain insights into the climate data.

## Flask API

The Flask API provides endpoints to access climate data from the Hawaii database. The API is designed to serve various requests for precipitation data, temperature observations, and station information.

### Available Routes:

- **Homepage:** `/` - Lists all available routes.
- **Precipitation Data:** `/api/v1.0/precipitation` - Returns precipitation data for the last 12 months.
- **Stations:** `/api/v1.0/stations` - Returns a list of stations.
- **Temperature Observations:** `/api/v1.0/tobs` - Returns temperature observations for the previous year.
- **Temperature Statistics by Start Date:** `/api/v1.0/<start>` - Returns temperature statistics for a specified start date.
- **Temperature Statistics by Start and End Dates:** `/api/v1.0/<start>/<end>` - Returns temperature statistics for a specified start and end date range.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
