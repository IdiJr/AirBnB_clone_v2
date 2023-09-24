#!/usr/bin/python3
"""
Script that starts a Flask web application
that listens on 0.0.0.0, port 5000
Routes:
/: display “Hello HBNB!”
/hbnb: display “HBNB”
/c/<text>: display “C ” followed by the value of the text variable
           (replace underscore _ symbols with a space)
/python/(<text>): display “Python ”, followed by the value of the text variable
                  (replace underscore _ symbols with a space)
                  The default value of text is “is cool”
/number/<n>: display “n is a number” only if n is an integer
/number_template/<n>: display a HTML page only if n is an integer:
                        H1 tag: “Number: n” inside the tag BODY
/number_odd_or_even/<n>: display a HTML page only if n is an integer:
                        H1 tag: “Number: n is even|odd” inside the tag BODY
"""
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_route():
    """
    Return string “Hello HBNB!”
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_route():
    """
    Return string “HBNB”
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """
    Returns string "C" followed by the value of the text variable
    """
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is cool"):
    """
    Returns string "Python " followed by the value of the text variable
    """
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<int:num>", strict_slashes=False)
def number_route(num):
    """
    Return "n is a number" if "num" is an integer
    """
    return "{} is a number".format(num)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template_route(n):
    """
    Returns an HTML page if "n" is an integer
    """
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>")
def number_odd_or_even_route(n):
    """
    Returns an HTML page if n is an integer
    """
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
