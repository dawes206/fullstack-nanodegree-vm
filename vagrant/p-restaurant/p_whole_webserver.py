#You wanted to put each html page into a separate file have webserver serve them up as needed. You got it to work, but there's an issue. You can't manipulate the html files.
#Instead, you will include the html strings here, likely copied over from the working html files for accuracy, and then just insert the values that you need using string manipulation
#You can still keep the database_connection.py file separate, and just reference it's functions in this script. You also got that working.
#Right now you just finished making the test case work, which serves up the test page html with the testFunc return value added in.
#Next thing you should do is STOP! Look at more of the course info. Know what they want you to do. Relax!!! There are literally objectives. It's possible that he has a different approach entirely.
#Think about what you would have your code do. Really think about it. Map it out on paper, maybe. Know what you would do, be able to explain it, and then go on. Be happy with knowing you COULD do it your way.
#But, at the end of the day, do it the way that will take the least work (following his approach). That's a skill you desperately need
#COnsider adding a database to your local machine inestad of just the vm, if possible. It would be awesome if I could just run the script here

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from os import curdir, sep

from database_connection import testFunc
from database_connection import getRestaurantNames

#html will have {} where I want to insert values
testHTML = '''<html>
  <body>
    <h1>Hello!</h1>
    <pre>{}</pre>
  </body>
</html>'''

restaurantsHTML = '''<html>
  <body>
     <pre>{}</pre>
  </body>
</html>'''




class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #test = open('index.html')
                #self.wfile.write(test.read().encode())
                return
            if self.path == '/restaurants':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #test = open('restaurants.html')
                #self.wfile.write(test.read().encode())
                restaurantNames = getRestaurantNames()
                restaurantNamesString = '\n'.join(restaurantNames)
                self.wfile.write(restaurantsHTML.format(restaurantNamesString).encode())
                return
            if self.path == '/restaurants/new':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #test = open('new_restaurants.html')
                #self.wfile.write(test.read().encode())
                return
            if self.path == '/restaurant/id/edit':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #test = open('edit_restaurant.html')
                #self.wfile.write(test.read().encode())
                return
            if self.path == '/test':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #test = open('edit_restaurant.html')
                #self.wfile.write(test.read().encode())
                self.wfile.write(testHTML.format(testFunc()).encode()) #.format html strings to input values that I want. These values can come from dtabase_connection's functions
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)
                return




def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
