import datetime
from project import db


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