import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import create_engine
from flask import jsonify
# SQLite Database setup for the final project and SQLAlchemy

Base = declarative_base()

# Classes for the tables in the DB
# Assumptions for sake of project - An artist can sing many songs, 
# and songs can only be sung by one artist 
# Artist <-1----N-> Song

# Personal note - association tables to show many to many relationships with sqlalchemy
class Artist(Base):
	__tablename__ = 'artist'

	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)

class Song(Base):
	__tablename__ = 'song'

	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	length = Column(String(80), nullable=True)

	artist_id = Column(Integer, ForeignKey('artist.id', ondelete='CASCADE'))
	artist = relationship('Artist', backref=backref(__tablename__, cascade='all,delete'))

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'length': self.length
		}

engine = create_engine('sqlite:///artistsong.db')
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
