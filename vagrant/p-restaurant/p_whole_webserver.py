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
import cgitb
cgitb.enable()
from os import curdir, sep

from database_connection import testFunc
from database_connection import getRestaurantNames
from database_connection import addRestaurant
from databse_connection import getRestaurantData


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

newRestaurantsHTML = '''<html>
  <body>
    <h1>new restaurant!</h1>
    <form method=POST enctype='multipart/form-data' action="/restaurants/new">
      <input type=text name = restaurantName>
      <input type="submit" value="Submit">
    </form>
    <p>testing</p>
  </body>
</html>'''




class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                return
            if self.path == '/restaurants':
                restaurantNames = getRestaurantNames()

                message = ''
                message += '<html><body>'
                for i in restaurantNames:
                    message += '<p>{}</p>'.format(i)
                    message += '<a href =/restaurant/id/edit>Edit </a>' #id can be changed to a {} and filled in with the database id number of the restaurant.
                    message += '<a href =/restaurant/id/delete>Delete</a>'
                message += '<br/>'
                message += '<a href = /restaurants/new>New Restaurant</a>'
                message += '</body></html>'

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(message.encode())
                return
            if self.path == '/restaurants/new':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(newRestaurantsHTML.encode())


                return
            if self.path == '/restaurant/id/edit': #if self.path matches patter restaurant/*/edit, create webpage that has other data pulled from database based on the id# given
                #parse self.path string to get value of id. It will always be the same pace, so do self.path[11:(location of 3rd /)]
                #set get restaurant row using newly defined function getRestaurantData from database_connection. restaurantRow = getRestaurantData(input = id)
                #html
                    #restaurantRow.name
                    #form where input field is text and has restaurantRow.name as placeholder (or maybe input. Whichever one will let you edit instead of just overwriting)
                    #form input field has name editedRestaurantName
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                return
            if self.path == '/restaurant/id/delete':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                return
            if self.path == '/test':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(testHTML.format(testFunc()).encode()) #.format html strings to input values that I want. These values can come from dtabase_connection's functions
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)
                return
    def do_POST(self):
        #if self.path == '/restaurants/new': Have to distinguis between forms coming from different parts of the server.
        ctype, pdict = cgi.parse_header(self.headers.get('content-type')) #Type needs to be certain type so we can get pdict
        pdict['boundary'] = pdict['boundary'].encode('utf-8') #pdict needs to be in bytes
        fields = cgi.parse_multipart(self.rfile, pdict) #parse the input file based on dictionary of parameters
        formRestaurant = fields['restaurantName'][0].decode('utf-8') #decode new restaurant name into string
        addRestaurant(formRestaurant)

        #redirect to restaurants page
        self.send_response(303)
        self.send_header('location','/restaurants')
        self.end_headers()

        #if self.path matches the patter of an edit page....
        #parse data using above method (or method from bookmark server).
        #Decode and read the value of editedRestaurantName.
        #restaurant = getRestaurantData(id (pulled from self.path))
        #restaurant.name = editedRestaurantName
        #session.add(restaurant)
        #session.commit()

        #redirect to restaurant page with a 303 response (see above)


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
