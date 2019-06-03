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
import re #to perform regex comparison

from database_connection import testFunc
from database_connection import getRestaurantNames
from database_connection import addRestaurant
from database_connection import getRestaurantData
from database_connection import getRestaurants
from database_connection import commitData
from database_connection import deleteRestaurant


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

editRestaurantHTML = '''<html>
  <body>
    <h1>Edit {}</h1>
    <form method=POST enctype='multipart/form-data' action="/restaurant/{}/edit">
      <input type=text name = editedRestaurantName value = {}>
      <input type="submit" value="Submit">
    </form>
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
                restaurantNames = getRestaurantNames() #good for when you just need a list of restaurant names (objective 1).

                restaurants = getRestaurants() #good for when you need restaurant names and id's (objective 4)

                message = ''
                message += '<html><body>'
                for restaurant in restaurants:
                    message += '<p>{}</p>'.format(restaurant.name)
                    message += '<a href =/restaurant/{}/edit>Edit </a>'.format(restaurant.id) #id can be changed to a {} and filled in with the database id number of the restaurant.
                    message += '<a href =/restaurant/{}/delete>Delete</a>'.format(restaurant.id)
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
            if re.search('restaurant/[0-9]*/edit',self.path):
                id = self.path[12:-5]
                try:
                    id = int(id)
                except:
                    print('id not a number')
                restaurantRow = getRestaurantData(id)
                #html
                message = '<html><body>'
                message += '<h1>Edit {}</h1>'.format(restaurantRow.name)
                message += "<form method=POST enctype='multipart/form-data' action='/restaurant/{}/edit'>".format(restaurantRow.id)
                message += '''<input type=text name = editedRestaurantName value = "{}">'''.format(restaurantRow.name)
                message += "<input type='submit' value='Submit'>"
                message += "</form></body></html>"


                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(message.encode())

                return
            if re.search('restaurant/[0-9]*/delete',self.path):#if page matches delete page pattern
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #get restaurant row info using path
                id = self.path[12:-7]
                try:
                    id = int(id)
                except:
                    print('id not a number')
                restaurantRow = getRestaurantData(id)

                #html
                message = ''
                message = '<html><body>'
                message += '<h1>Are you sure you want to delete {}</h1>'.format(restaurantRow.name)
                message += "<form method=POST enctype='multipart/form-data' action='/restaurant/{}/delete'>".format(restaurantRow.id)
                message += "<input type='submit' value='Delete'>"
                message += "</form></body></html>"

                self.wfile.write(message.encode())


                return
            if self.path == '/test':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(testHTML.format(testFunc()).encode())
                self.send_error(404, 'File Not Found: %s' % self.path)
                return
    def do_POST(self):
        if self.path == '/restaurants/new':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = pdict['boundary'].encode('utf-8')
            fields = cgi.parse_multipart(self.rfile, pdict)
            formRestaurant = fields['restaurantName'][0].decode('utf-8')
            addRestaurant(formRestaurant)

            #redirect to restaurants page
            self.send_response(303)
            self.send_header('location','/restaurants')
            self.end_headers()

        if re.search('restaurant/[0-9]*/edit',self.path):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = pdict['boundary'].encode('utf-8')
            fields = cgi.parse_multipart(self.rfile, pdict)
            editedName = fields['editedRestaurantName'][0].decode('utf-8')
            id = self.path[12:-5]
            try:
                id = int(id)
            except:
                print('id not a number')
            restaurant = getRestaurantData(id)
            restaurant.name = editedName
            commitData(restaurant)

            self.send_response(303)
            self.send_header('location','/restaurants')
            self.end_headers()

        if re.search('restaurant/[0-9]*/delete',self.path):
            id = self.path[12:-7]
            try:
                id = int(id)
            except:
                print('id not a number')
            #get restaurant using getRestaurantData
            restaurant = getRestaurantData(id)
            #delete restaurant using new deleteRestaurant function
            deleteRestaurant(restaurant)

            #redirect to restaurants page
            self.send_response(303)
            self.send_header('location','/restaurants')
            self.end_headers()

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
