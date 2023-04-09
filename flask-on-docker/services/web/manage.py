from flask.cli import FlaskGroup

from project import app
from project import db
from project.models import *


cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(email="aditnegi1@gmail.com"))
    db.session.commit()


if __name__ == "__main__":
    cli()
