#!/usr/bin/python3
"""
Script that starts a Flask web application
that listens on 0.0.0.0, port 5000
Routes:
    /cities_by_states: display a HTML page: (inside the tag BODY)
    H1 tag: “States”
    UL tag: with the list of all State objects present in DBStorage
    sorted by name (A->Z)
    LI tag: description of one State: <state.id>: <B><state.name></B>
    /states/<id>: display a HTML page: (inside the tag BODY)
    If a State object is found with this id:
        H1 tag: “State: ”
        H3 tag: “Cities:”
        UL tag: with the list of City objects linked to the State
        sorted by name (A->Z)
        LI tag: description of one City: <city.id>: <B><city.name></B>
"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.city import City
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def cities_by_states():
    """
    Returns an HTML page that dispalys states objects in DBstorage sorted
    by name (A-Z)
    """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template("8-cities_by_states.html", states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """
    Returns an HTML page that dispalys states and city objects in DBstorage
    sorted by name (A-Z)
    """
    state = storage.get(State, id)
    if state:
        cities = sorted(state.cities, key=lambda city: city.name)
        return render_template('state_cities.html', state=state, cities=cities)
    else:
        return "Not found!", 404


@app.teardown_appcontext
def teardown(exc):
    """
    Closes SQLAlchemy session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
