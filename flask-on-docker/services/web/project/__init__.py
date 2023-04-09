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



