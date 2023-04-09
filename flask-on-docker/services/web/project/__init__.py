import os

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

BASE_URL = "/v1/api/"
@app.route("/")
def hello_world():
    return "Game of Papers API v1.0 Documentation"

@app.route(BASE_URL + "recommendations")
def hello_worl():
    return jsonify({"message": "Hello, World!"})

