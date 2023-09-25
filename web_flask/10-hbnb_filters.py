#!/usr/bin/python3
"""
Script that starts a Flask web application
that listens on 0.0.0.0, port 5000
Routes:
    /hbnb_filters: display a HTML page like 6-index.html
"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Returns an HTML page for hbnb_filters
    """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    cities = storage.all("City").values()
    sorted_states = sorted(states, key=lambda state: state.name)
    sorted_amenities = sorted(amenities, key=lambda amenity: amenity.name)
    sorted_cities = sorted(cities, key=lambda city: city.name)
    return render_template(
        "10-hbnb_filters.html",
        states=sorted_states,
        cities=sorted_cities,
        amenities=sorted_amenities
    )


@app.teardown_appcontext
def teardown(exc):
    """
    Closes SQLAlchemy session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
