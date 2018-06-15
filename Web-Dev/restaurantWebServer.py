from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
import cgi

#HTTPRequestHandler to handle HTTP protocols and requests between the client and the server
class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path.endswith('/restaurant'):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				restaurants = self.server.session.query(Restaurant).all()

				output = ""
				output += "<html><body>"
				output += "<h1>A list of Restaurants</h1>"

				for restaurant in restaurants:
					output += "<p><h2> %s </h2>" % restaurant.name
					output += "<a href='/restaurant/%d/edit'>Edit</a><br>" % restaurant.id
					output += "<a href='/restaurant/%d/delete'>Delete</a><br>" % restaurant.id
					output += "</p>"

				output += "<a href='/restaurant/new'>Add a new restaurant onto the list</a>"	
				output += "</body></html>"
				print(output)
				self.wfile.write(output.encode('utf-8'))
				
			elif self.path.endswith('/restaurant/new'):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Add a new restaurant</h1>"
				output += "<form action='/restaurant/new' method='POST' enctype='multipart/form-data'>"
				output += "Restaurant Name : <input type='text' name='new_restaurant_name'>"
				output += "<input type='submit' name='Submit'></form>"
				output += "</body></html>"
				print(output)
				self.wfile.write(output.encode('utf-8'))

			elif self.path.endswith('/edit'):	#TODO - fix later on to check for /restaurant/number/edit
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				r_id = self.path.split('/')[2]	#path should come in form of /a/b/c -> split extracts to ['', a, b, c]
				restaurant = self.server.session.query(Restaurant).filter_by(id=r_id).one()

				output = ""
				output += "<html><body>"

				if restaurant != []:
					output += "<h1>Rename %s</h1>" %  restaurant.name
					output += "<form action='/restaurant/%d/edit' method='POST' enctype='multipart/form-data'>" % restaurant.id
					output += "Enter new name here : <input type='text' name='edit_restaurant_name'>"
					output += "<input type='submit' name='Submit'>"
					output += "<input type='hidden' name='id' value=%d></form>" % restaurant.id
				else:
					raise IOError()

				output += "</body></html>"
				print(output)
				self.wfile.write(output.encode('utf-8'))

			elif self.path.endswith('delete'):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				r_id = self.path.split('/')[2]
				restaurant = self.server.session.query(Restaurant).filter_by(id=r_id).one()

				output = ""
				output += "<html><body>"

				if restaurant != []:
					output += "<h1>Are you sure you want to delete %s from the list of restaurants?</h1>" %  restaurant.name
					output += "<form action='/restaurant/%d/delete' method='POST' enctype='multipart/form-data'>" % restaurant.id
					output += "<input type='submit' name='yes_button' value='Yes'>"
					output += "<a href='/restaurant'><button type='button'>No</button></a>" #semantically bad by standards
					output += "<input type='hidden' name='id' value=%d></form>" % restaurant.id
				else:
					raise IOError()

				output += "</body></html>"
				print(output)
				self.wfile.write(output.encode('utf-8'))


		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.send_header('Content-type','text/html')
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
			pdict['boundary'] = pdict['boundary'].encode('utf-8')
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
			
			output = ""
			output += "<html><body>"

			restaurant = None
			#Handle POST requests from diff forms
			if self.path.endswith('/restaurant/new'): #getvalue returns empty string, a string, or a list of strings depending on use case
				content = fields.get('new_restaurant_name')
				restName = content[0].decode('utf-8')
				restaurant = Restaurant(name=restName)

				output += "<h1>%s has been added to the list of Restaurants</h1>" % restaurant.name
				output += "<a href='/restaurant'>Return to the list of restaurants</a>"

			elif self.path.endswith('/edit'):
				r_id = self.path.split('/')[2]
				content = fields.get('edit_restaurant_name')
				restaurant = self.server.session.query(Restaurant).filter_by(id=r_id).one()
				newName = content[0].decode('utf-8')

				#Check new name length and display corresponding message
				if len(newName) > 0:
					restaurant = self.server.session.query(Restaurant).filter_by(id=r_id).one()
					oldName = restaurant.name
					restaurant.name = newName

					output += "<h1>%s has been renamed to %s</h1>" % (oldName, newName)	
				else:
					output +="<h1>Invalid name. Please input a name that has a length greater than 0.</h1>"

				output += "<a href='/restaurant'>Return to the list of restaurants</a>"

			elif self.path.endswith('/delete'):
				r_id = self.path.split('/')[2]
				restaurant = self.server.session.query(Restaurant).filter_by(id=r_id).one()
				r_name = restaurant.name
				self.server.session.delete(restaurant)
				self.server.session.commit()
				output += "<h1>%s has been deleted from the list</h1>" % r_name 
				output += "<a href='/restaurant'>Return to the list of restaurants</a>"

			output += "</html></body>"
			#maybe belongs in each specific if-else block - in case deadlock. exa: Message shows to client but doesn't push to DB
			insp = inspect(restaurant)		#inspect state of object since delete commits inside another block of code

			if restaurant != None and not insp.detached:
				self.server.session.add(restaurant)
				self.server.session.commit()

			print(output)
			self.wfile.write(output.encode('utf-8'))

		except Exception as e:
			print(e)


def main():
	try:
		engine = create_engine('sqlite:///restaurantmenu.db')
		Base.metadata.bind=engine
		DBSession = sessionmaker(bind=engine)

		port = 8080
		server = HTTPServer(('', port), CustomHTTPRequestHandler)
		print('Restaurant Web Server is up and running...')
		server.session = DBSession()
		print('DBSession setup complete')
		server.serve_forever()	

	except KeyboardInterrupt: #Ctrl-C to stop server running
		print('^C entered - the web server will now stop')
		server.socket.close()

if __name__ == '__main__':
	main()
