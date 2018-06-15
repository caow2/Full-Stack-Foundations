from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#route decorators bind a function to a url -> function routes to both '/' and 'hello'
#stacking route decorators specifies two pages for the same function
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')	#dynamic path -> path/<type:variable_name>/path to substitute var name
def restaurantMenu(restaurant_id=1):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/all')
def displayAll():
	restaurants = session.query(Restaurant).all()
	output = ''
	print(restaurants)
	if restaurants == []:
		output += 'No restaurant information was found.'
	else:
		for restaurant in restaurants:
			output += '<strong>' + restaurant.name + '</strong><br>'
			items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)

			if items == []:
				print('No menu items found')
				continue

			for item in items:
				output += '&nbsp&nbsp&nbsp&nbsp' + item.name + '<br>'
				output += '&nbsp&nbsp&nbsp&nbsp' + item.price + '<br>'
				output += '&nbsp&nbsp&nbsp&nbsp' + item.description + '<br>'
				output += '<br>'
	return output

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['POST','GET'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
    	item = MenuItem(name=request.form['item_name'], restaurant_id=restaurant_id)
    	session.add(item)
    	session.commit()
    	flash("%s has been added to the menu" % item.name)
    	return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
    	return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['POST','GET'])
def editMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		oldname = item.name
		item.name = request.form['new_name']
		session.add(item)
		session.commit()
		flash("%s has been changed to %s" % (oldname, item.name))
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, item=item)

    
# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash("%s has been removed from the menu" % item.name)
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deleteitem.html', restaurant_id=restaurant_id, item=item)

#Making API Endpoints
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	return jsonify(MenuItems=[item.serialize for item in items])	#serialize all menu items for restaurant

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
	return jsonify(MenuItem=item.serialize)

if __name__ == '__main__':	#only execute if running from interpreter
	app.secret_key = 'key'
	app.debug = True
	app.run(host = '0.0.0.0', port=5000)

#The above will evaluate to False if project.py is use as an imported module
#host = '0.0.0.0' tells server to listen on all public IP addresses
#Setting debug to True allows the server to reset itself each time code is changed -> don't have to manually restart server