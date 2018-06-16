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
	if songs == []:
		return "No songs were available for artist %s" % artist.name
	return render_template('songs.html', artist=artist, songs=songs)

@app.route('/artists/<int:artist_id>/edit/', methods=['GET', 'POST'])
def editArtist(artist_id):
	artist = session.query(Artist).filter_by(id=artist_id).one()
	if request.method == 'GET':
		return render_template('editArtist.html', artist=artist)
	elif request.method == 'POST':
		artist.name = request.form.get('newname')
		session.add(artist)
		session.commit()
		return redirect(url_for('allArtists'))

@app.route('/artists/new/', methods=['GET','POST'])
def newArtist():
	if request.method == 'GET':
		return render_template('newArtist.html')
	elif request.method == 'POST':
		new_artist = Artist(name=request.form.get('artist_name'))
		session.add(new_artist)
		session.commit()
		return redirect(url_for('allArtists'))

@app.route('/artists/<int:artist_id>/delete/', methods=['GET','POST'])
def deleteArtist(artist_id):
	artist = session.query(Artist).filter_by(id=artist_id).one()
	if request.method == 'GET':
		return render_template('deleteArtist.html', artist=artist)
	elif request.method == 'POST':
		session.delete(artist)
		session.commit()
		return redirect(url_for('allArtists'))

@app.route('/artists/<int:artist_id>/songs/<int:song_id>/edit/', methods=['GET','POST'])
def editSong(artist_id, song_id):
	song = session.query(Song).filter_by(id=song_id).one() #utilize song's artist reference
	if request.method == 'GET':
		return render_template('editSong.html', artist=song.artist, song=song)
	elif request.method == 'POST':
		song.name = request.form.get('song_name')
		session.add(song)
		session.commit()
		return redirect(url_for('artistSongs', artist_id=song.artist.id))

@app.route('/artists/<int:artist_id>/songs/<int:song_id>/delete/', methods=['GET', 'POST'])
def deleteSong(artist_id, song_id):
	song = session.query(Song).filter_by(id=song_id).one()	#better to utilize parameter artist_id - song.artist.id is invalid after it has been deleted from DB
	if request.method == 'GET':
		return render_template('deleteSong.html', artist=song.artist, song=song)
	elif request.method == 'POST':
		session.delete(song)
		session.commit()
		return redirect(url_for('artistSongs', artist_id=artist_id)) 

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)