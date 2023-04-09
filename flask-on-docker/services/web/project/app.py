from flask import (
    jsonify,
    send_from_directory,
    request,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from project import app

BASE_URL = "/v1/api/"


@app.route("/")
def hello_world():
    return "Game of Papers API v1.0 Documentation"

@app.route(BASE_URL + "recommendations")
def hello_worl():
    return jsonify({"message": "Hello, World!"})



@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return """
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """
