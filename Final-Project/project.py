from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Artist, Song

app = Flask(__name__)

engine = create_engine('sqlite:///artistsong.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/artists/')
def allArtists():
	artists = session.query(Artist).all()
	if artists == []:
		return "No artist data was available"
	return render_template('artists.html', artists=artists)

@app.route('/artists/<int:artist_id>/songs/')
def artistSongs(artist_id):
	artist = session.query(Artist).filter_by(id=artist_id).one()
	songs = session.query(Song).filter_by(artist_id=artist_id)
	print(songs)
	if songs == []:
		return "No songs were available for artist %s" % artist.name
	return render_template('songs.html', artist=artist, songs=songs)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)