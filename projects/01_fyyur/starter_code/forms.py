from datetime import datetime
import re
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError, Regexp

# from .app import Artist
from value_object.genre import Genre

state_choices = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
]


def is_valid_phone(form, phone):
    regex = re.compile('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
    if not regex.match(phone.data):
        raise ValidationError('wrong phone number')

class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state_choices,
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired(), is_valid_phone]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices(),
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField('seeking_talent')

    seeking_description = StringField(
        'seeking_description'
    )

    def validate_genres(self, genres):
        s_genres = set(genres.data)
        if s_genres != (s_genres & {g.value for g in Genre}):
            raise ValidationError('not select from genre')

    def set_data(self, venue):
        self.name.data = venue.name
        self.city.data = venue.city
        self.state.data = venue.state
        self.address.data = venue.address
        self.genres.data = venue.genres.split(',')
        self.website_link.data = venue.website_link
        self.facebook_link.data = venue.facebook_link
        self.phone.data = venue.phone
        self.image_link.data = venue.image_link
        self.seeking_talent.data = venue.seeking_talent
        self.seeking_description.data = venue.seeking_description

    def feedback_to(self, venue):
        venue.name = self.name.data
        venue.city = self.city.data
        venue.state = self.state.data
        venue.address = self.address.data
        venue.phone = self.phone.data
        venue.genres = ','.join(self.genres.data)
        venue.image_link = self.image_link.data
        venue.facebook_link = self.facebook_link.data
        venue.website_link = self.website_link.data
        venue.seeking_talent = self.seeking_talent.data
        venue.seeking_description = self.seeking_description.data


class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state_choices
    )
    phone = StringField(
        'phone', validators=[DataRequired(), is_valid_phone]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices(),
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

    website_link = StringField(
        'website_link'
    )

    seeking_venue = BooleanField('seeking_venue')

    seeking_description = StringField(
        'seeking_description'
    )

    def validate_genres(self, genres):
        s_genres = set(genres.data)
        if s_genres != (s_genres & {g.value for g in Genre}):
            raise ValidationError('not select from genre')

    def set_data(self, artist):
        self.name.data = artist.name
        self.city.data = artist.city
        self.state.data = artist.state
        self.genres.data = artist.genres.split(',')
        self.website_link.data = artist.website_link
        self.facebook_link.data = artist.facebook_link
        self.phone.data = artist.phone
        self.image_link.data = artist.image_link
        self.seeking_venue.data = artist.seeking_venue
        self.seeking_description.data = artist.seeking_description

    def feedback_to(self, artist):
        artist.name = self.name.data
        artist.city = self.city.data
        artist.state = self.state.data
        artist.genres = ','.join(self.genres.data)
        artist.website_link = self.website_link.data
        artist.facebook_link = self.facebook_link.data
        artist.phone = self.phone.data
        artist.image_link = self.image_link.data
        artist.seeking_venue = self.seeking_venue.data
        artist.seeking_description = self.seeking_description.data
