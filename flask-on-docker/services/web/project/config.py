import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent configuration class."""
    #default to sqlite is postgres not present
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    print("Printing SQLALCHEMY_DATABASE_URI")
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/media"
