from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
import cgi

class webserverHandler(BaseHTTPRequestHandler):
	#Handles HTTP requests for HTTPServer
	def do_GET(self):
		try:
			if self.path.endswith("/hello"): #path contains URL sent by the client 
				self.send_response(200) #response code 200 indicates success
				self.send_header('Content-type', 'text/html') #indicates that the server is replying with html text
				self.end_headers() #blank line to indicate end of headers

				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
				output += "<h2>What would you like me to say?</h2>"
				output += "<input name='message' type='text'> <input type='submit' value ='Submit'> </form>"
				output += "</body></html>"
				self.wfile.write(bytes(output, "utf-8"))	#wfile contains output stream that responds back to client
															#write takes encoded bytes, not strings
				print(output) #debugging
				return

			if self.path.endswith("/hola"):
				self.send_response(200) 
				self.send_header('Content-type', 'text/html') 
				self.end_headers() 

				output = ""
				output += "<html><body>&#161Hola <br/> <a href='/hello'>Back to Hello</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
				output += "<h2>What would you like me to say?</h2>"
				output += "<input name='message' type='text'> <input type='submit' value ='Submit'> </form>"
				output += "</body></html>"
				self.wfile.write(bytes(output, "utf-8"))
				print(output) 
				return

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.get('content-type')) #parses into main value and dictionary of parameters
			pdict['boundary'] = bytes(pdict['boundary'],"utf-8") 
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict) #rfile - file to be read
				messagecontent = fields.get('message')

			output = ""
			output += "<html><body>"
			output += "<h2> Okay, how about this: </h2>"
			output += "<h1> %s </h1>" % messagecontent[0].decode("utf-8")	#messagecontent[0] is byte string -> b' prefix

			for item in messagecontent:
				print(str(item))

			#Form to get the data
			output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
			output += "<h2>What would you like me to say?</h2>"
			output += "<input name='message' type='text'> <input type='submit' value ='Submit'> </form>"
			output += "</body></html>"
			self.wfile.write(bytes(output, 'utf-8'))
			print(output)

		except IOError:
			self.send_error(404, "File")

			


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print("Web server running on port %s" % port)
		server.serve_forever()

		engine = create_engine('sqlite:///restaurantmenu.db')
		Base.metadata.bind=engine
		DBSession = sessionmaker(bind=engine)

	except KeyboardInterrupt:	#handles ctrl-c input
		print("^C entered, stopping web server")
		server.socket.close()

if __name__ == '__main__':
	main()