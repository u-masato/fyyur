from datetime import datetime


from config import db


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    @property
    def artist_name(self):
        return self.artist.name

    @property
    def artist_image_link(self):
        return self.artist.image_link

    @property
    def venue_name(self):
        return self.venue.name

    @property
    def venue_image_link(self):
        return self.venue.image_link

    @property
    def start_time_str(self):
        return self.start_time.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def upcoming(self):
        return self.start_time >= datetime.today()


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue')

    @property
    def upcoming_shows(self):
        return list(filter(lambda show: show.start_time >= datetime.today(), self.shows))

    @property
    def upcoming_shows_count(self):
        return len(list(filter(lambda show: show.start_time >= datetime.today(), self.shows)))

    @property
    def past_shows(self):
        return list(filter(lambda show: show.start_time < datetime.today(), self.shows))

    @property
    def past_shows_count(self):
        return len(list(filter(lambda show: show.start_time < datetime.today(), self.shows)))


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
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist')

    @property
    def upcoming_shows(self):
        return list(filter(lambda show: show.start_time >= datetime.today(), self.shows))

    @property
    def upcoming_shows_count(self):
        return len(list(filter(lambda show: show.start_time >= datetime.today(), self.shows)))

    @property
    def past_shows(self):
        return list(filter(lambda show: show.start_time < datetime.today(), self.shows))

    @property
    def past_shows_count(self):
        return len(list(filter(lambda show: show.start_time < datetime.today(), self.shows)))
