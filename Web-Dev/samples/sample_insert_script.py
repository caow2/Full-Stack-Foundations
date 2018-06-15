#Full stack tutorial -> SQLAlchemy - populate the DB

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db') #
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine) #SQLAlchemy works with DB thru session -> DB connection
session = DBSession() #Creates instance of connection to the DB, but changes won't be pushed
					  #to the DB until commit() is called

'''	New Entries can be inserted into the DB take the following format
 	Entry = ClassName(property="some value", etc...)
 	session.add(newEntry)
 	session.commit() '''

newRestaurant = Restaurant(name="Pizza Palace")
session.add(newRestaurant)
session.commit()

newPizza = MenuItem(name="Cheese Pizza",
 				  description="The most basic pizza ever.",
 				  course="Entree",
 				  price="9.99",
 				  restaurant=newRestaurant)
session.add(newPizza)
session.commit()

allRestaurant = session.query(Restaurant).all() #Query the session's DB for all rows in Restaurant table - 
 								 	   			#returns an object
allMItem = session.query(MenuItem).all()

firstRest = session.query(Restaurant).first()
print(firstRest.name)

