from flask_sqlalchemy import SQLAlchemy

from app import db


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    artists = db.relationship('Artist', secondary='shows', backref=db.backref('artists', lazy=True))


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    venues = db.relationship('Venue', secondary='shows', backref=db.backref('venues', lazy=True))


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

shows = db.Table('shows',
                 db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
                 db.Column('artist.id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
                 db.Column('start_time', db.DateTime, nullable=False),
                 )
