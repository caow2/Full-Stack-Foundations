#Insert data into artistsong.db
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Artist, Song

engine = create_engine('sqlite:///artistsong.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def commit(artist, *songs):
	session.add(artist)
	for song in songs:
		session.add(song)
	session.commit()

#Artist 1
artist1 = Artist(name='Tracy Chapman')

song1 = Song(name='Fast Car', length='4:26')
song2 = Song(name='Give Me One Reason', length='4:07')
song3 = Song(name='Stand By Me', length='2:49')
song4 = Song(name='Say Hallelujah', length='2:08')
commit(artist1, song1, song2, song3, song4)

#Artist 2
artist2 = Artist(name='Neil Young')

song1 = Song(name='Heart of Gold', length='3:07')
song2 = Song(name='Ohio', length='3:00')
song3 = Song(name='Sugar Mountain', length='5:47')
song4 = Song(name='Harvest Moon', length='5:41')
song5 = Song(name='Old King', length='2:57')
song6 = Song(name='Unknown Legend', length='4:32')
commit(artist2, song1, song2, song3, song4, song5, song6)

#Artist 3
artist3 = Artist(name='Nick Cave')

song1 = Song(name="(Are You) The One That I've Been Waiting For?", length='4:05')
song2 = Song(name="Into My Arms", length='4:15')
song3 = Song(name="Love Bomb", length='4:26')
song4 = Song(name="Grinderman", length='4:33')
commit(artist3, song1, song2, song3, song4)