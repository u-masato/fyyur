# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import render_template, request, flash, redirect, url_for, abort, jsonify
from sqlalchemy import cast, Date
import logging
from logging import Formatter, FileHandler
from forms import *

from config import app, db
# import models
from models import Venue, Artist, Show


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues_sorted_by_area = Venue.query.order_by(Venue.state).all()

    data = []
    state = None
    for venue in venues_sorted_by_area:
        if venue.state != state:
            data.append({
                "city": venue.city,
                "state": venue.state,
                "venues": []
            })
            state = venue.state
        data[-1]["venues"].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": venue.upcoming_shows_count
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{term}%')).all()

    def count_upcoming_shows(_shows):
        return len(list(filter(lambda show: show.start_time >= datetime.today(), _shows)))

    response = {
        'count': len(venues),
        'data': [{'id': venue.id, 'name': venue.name, 'num_upcoming_shows': count_upcoming_shows(venue.shows)}
                 for venue in venues]
    }

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.filter_by(id=venue_id).one()
    return render_template('pages/show_venue.html', venue=venue)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    form = VenueForm()
    if not form.validate_on_submit():
        message = []
        for key, errors in form.errors.items():
            message.append("|".join(errors))
        flash(f'Error: {str(message)}')
        return redirect(url_for('create_venue_form'))

    # on successful db insert, flash success
    try:
        venue = Venue()
        form.feedback_to(venue)
        db.session.add(venue)
        db.session.commit()
    except BaseException as e:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    result = False
    try:
        venue = Venue.query.filter_by(id=venue_id).one()
        db.session.delete(venue)
        Show.query.filter_by(venue_id=venue_id).delete()
        db.session.commit()
        result = True
    except Exception as e:
        print(e.args)
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({
        'delete': result
    })


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artists= Artist.query.all()
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{term}%')).all()
    response = {
        "count": len(artists),
        "data": [{
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": artist.upcoming_shows_count,
        } for artist in artists]
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    artist = Artist.query.filter_by(id=artist_id).first()
    if not artist:
        abort(404)
    return render_template('pages/show_artist.html', artist=artist)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()
    if not artist:
        # error
        abort(404)

    form.set_data(artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()

    if not form.validate_on_submit():
        message = []
        for key, errors in form.errors.items():
            message.append("|".join(errors))
        flash(f'Error: {message[0]}')
        return redirect(url_for('artists'))

    form.feedback_to(artist)

    try:
        db.session.commit()
    except BaseException as e:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).first()

    if not venue:
        # error
        abort(404)

    form.set_data(venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).first()

    if not venue:
        # error
        abort(404)
    if not form.validate_on_submit():
        message = []
        for key, errors in form.errors.items():
            message.append("|".join(errors))
        flash(f'Error: {str(message)}')
        return redirect(url_for('venues'))

    form.feedback_to(venue)
    try:
        db.session.commit()
    except BaseException as e:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    form = ArtistForm()

    if not form.validate_on_submit():
        message = []
        for key, errors in form.errors.items():
            message.append("|".join(errors))
        flash(f'Error: {str(message)}')
        return redirect(url_for('artists'))

    artist = Artist()
    form.feedback_to(artist)
    try:
        db.session.add(artist)
        db.session.commit()
    except BaseException as e:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    # on successful db insert, flash success
    if error:
        flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
    else:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    _shows = Show.query.all()
    show_data = [{
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')} for show in _shows]

    return render_template('pages/shows.html', shows=show_data)


@app.route('/shows/create', methods=['GET'])
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    form = ShowForm()

    if form.validate_on_submit():
        show = Show(artist_id=form.artist_id.data,
                    venue_id=form.venue_id.data,
                    start_time=form.start_time.data)

        try:
            db.session.add(show)
            db.session.commit()
        except BaseException as e:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
    else:
        error = True

    # on successful db insert, flash success
    if error:
        flash('An error occurred. Show could not be listed.')
    else:
        flash('Show was successfully listed!')

    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/shows/search', methods=['POST'])
def search_shows():
    term = request.form.get('search_term', '')
    if not term:
        term = datetime.now()
    try:
        shows = db.session.query(Show).join(Artist).join(Venue).\
            filter(cast(Show.start_time, Date) >= cast(term, Date)).all()
    except:
        # invalid date format
        shows = []

    response = {
        'count': len(shows),
        'data': [{'id': show.id,
                  'show': show,
                  'artist': show.artist,
                  'venue': show.venue,
                  'start_time': str(show.start_time),
                  } for show in shows]
    }

    return render_template('pages/show.html', results=response,
                           search_term=request.form.get('search_term', ''))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
