import os

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    send_file
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

import datetime
from io import BytesIO


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
CORS(app)


class User(db.Model):
    '''User model'''
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        '''Initialize the user object'''
        self.email = email

class ResearchPapers(db.Model):
    '''Reseach paper model model'''
    __tablename__ = "research_papers"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    paper_id = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    version = db.Column(db.Integer, default=1, nullable=True)
    title = db.Column(db.String(256), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    authors = db.Column(db.JSON, nullable=True)
    conference = db.Column(db.String(128), nullable=True)
    recommendations = db.Column(db.JSON, nullable=True)
    paper_published_at = db.Column(db.String(128), nullable=True)
    paper = db.Column(db.LargeBinary, nullable=True)
    

    def __init__(self, paper_id):
        '''Initialize the user object'''
        self.paper_id = paper_id


#application code
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


BASE_URL = "/v1/api/"
@app.route("/")
def hello_world():
    return "Game of Papers API v1.0 Documentation"

@app.route(BASE_URL + "papers")
def list_papers():
    start = request.args.get("start")
    end = request.args.get("end")
    if start is None and end is None:
        start = 0
        end = 20
    if start is None:
        start = 0
        end = 20
    if end is None:
        start = int(start)
        end = start+20
    start, end = int(start), int(end)
    conference = request.args.get("conference")
    title = request.args.get("title")
    query = ResearchPapers.query

    if title:
        query = query.filter(ResearchPapers.title.ilike(f'%{title}%'))

    if conference:
        query = query.filter_by(conference=conference)

    papers = query.offset(start).limit(end - start + 1).all()

    result = []
    result = []
    cnt = 0
    for paper in papers:

        paper_data = {
            "id": paper.id,
            "title": paper.title,
            "author": paper.authors,
            "abstract": paper.abstract,
            "recommendations": paper.recommendations,
            "conference": paper.conference,
        }
        result.append(paper_data)

    return jsonify(result)

@app.route(BASE_URL + "papers/<id>")
def get_paper_by_id(id):
 
    paper = ResearchPapers.query.filter_by(id=id).first()
    if paper is None:
        return jsonify({"message": "Paper not found"}), 404
    paper_data = {
        "id": paper.id,
        "title": paper.title,
        "author": paper.authors,
        "abstract": paper.abstract,
        "conference": paper.conference,
        "paper_published_at": paper.paper_published_at,
        "recommendations": paper.recommendations,
        "created_at": paper.created_at,
        "updated_at": paper.updated_at,
        "version": paper.version,
        "active": paper.active,


    }
    return jsonify(paper_data)

@app.route(BASE_URL + "papers/<id>/pdf")
def get_paper_pdf_by_id(id):

    paper = ResearchPapers.query.filter_by(id=id).first()
    if paper:
        pdf_data = BytesIO(paper.paper)
        return send_file(pdf_data, mimetype='application/pdf', as_attachment=True, download_name=paper.title)
    else:
        return "Paper not found", 404
