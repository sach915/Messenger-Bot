import flask
import requests
import os

app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    print("Im in here")
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)
