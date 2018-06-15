from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

### Reading ###
#print all menu items
items = session.query(MenuItem).all()
for item in items:
	print(item.name)

#Column info
col_desc = session.query(MenuItem).column_descriptions

#Count - same thing
itemcount = session.query(MenuItem).count()
itemcount = session.query(func.count(MenuItem.id)).scalar()



### Updating ###
''' 1. Find the entry from the DB
	2. Modify the values
	3. Add to session and commit '''
veggieBurgers = session.query(MenuItem).filter_by(name="Veggie Burger") #all rows that match criteria
for burger in veggieBurgers:
	print(burger.id)
	print(burger.price)
	print(burger.restaurant.name + "\n")

pandaVBurger = session.query(MenuItem).filter_by(id=21).one() #one() brings back a row and converts automatically to object
															  #don't need for loop to access item

print(pandaVBurger.price)
pandaVBurger.price = '4.99'
session.add(pandaVBurger)
session.commit()			

#Update all burgers
for burger in veggieBurgers:		#veggieBurgers is dynamic - updates values when they are changed
	if burger.price != '2.99':
		burger.price = '2.99'
		session.add(burger)
		session.commit()	

for burger in veggieBurgers:
	print(burger.id)
	print(burger.price)
	print(burger.restaurant.name + "\n")	



### Delete ###
pandaBurger = session.query(MenuItem).filter_by(id=21).one()
session.delete(pandaBurger)
session.commmit()
pandaBurger = session.query(MenuItem).filter_by(id=21).one()
