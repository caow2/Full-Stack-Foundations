import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship #handles foreign key relationship
from sqlalchemy import create_engine #engines used for connecting

Base = declarative_base() #lets SQLAlchemy know that classes correspond to tables in the DB

#Classes for the Tables in the DB (extends declarative base)
#Mappers
class Restaurant(Base):
	__tablename__ = 'restaurant'

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)

class MenuItem(Base):
	__tablename__ = 'menu_item'

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))

	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

	restaurant = relationship(Restaurant)

	#Serialize function to enable sending JSON objects in serializable format
	@property
	def serialize(self):
		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'course': self.course,
			'price': self.price,
		}




# Insert at end of file #
engine = create_engine('sqlite:///restaurantmenu.db') #holds the connection (String?) to the DB
Base.metadata.create_all(engine) #goes into DB and adds the necessary classes as tables in the DB
