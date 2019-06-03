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
                # restaurantNamesString = '\n'.join(restaurantNames)
                print('test')

                message = ''
                message += '<html><body>'
                for i in restaurantNames:
                    message += '<p>{}</p>'.format(i)
                    message += '<a href =/restaurant/id/edit>Edit </a>'
                    message += '<a href =/restaurant/id/delete>Delete</a>'
                message += '</body></html>'

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # self.wfile.write(restaurantsHTML.format(restaurantNamesString).encode())
                self.wfile.write(message.encode())
                return
            if self.path == '/restaurants/new':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # test = open('new_restaurants.html')
                #self.wfile.write(test.read().encode())
                self.wfile.write(newRestaurantsHTML.encode())


                return
            if self.path == '/restaurant/id/edit':
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
    #Trying to get do_POST to actually work. It doesn't seem to be doing anything, but I think that's because I don't really understand what happense when I submit a form
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type')) #Type needs to be certain type so we can get pdict
        # pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['boundary'] = pdict['boundary'].encode('utf-8') #pdict needs to be in bytes
        fields = cgi.parse_multipart(self.rfile, pdict) #parse the input file based on dictionary of parameters
        formRestaurant = fields['restaurantName'][0].decode('utf-8') #decode new restaurant name into string

        addRestaurant(formRestaurant)


        #redirect to restaurants page
        self.send_response(303)
        self.send_header('location','/restaurants')
        self.end_headers()

        # self.send_response(200)
        # self.send_header('content-type','text/html')
        # self.end_headers()
        # message = ""
        # message += "<html><body>"
        # # message += "<h1> %s </h1>" % form['name'].value
        # # message += "<h1>%s</h1>" %self.headers.get('content-type')
        # # message += "<h1>%s</h1>" %self.rfile.read(int(self.headers.get('content-length'))).decode()
        # message += "<h1>%s</h1>"
        # message += "</body></html>"
        # self.wfile.write(message.encode())







        # try:
        #     self.send_response(200)
        #     self.send_header('content-type','text/html')
        #     self.end_headers()
        #
        #     ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        #     pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        #     if ctype == 'multipart/form-data':
        #         fields = cgi.parse_multipart(self.rfile, pdict)
        #         messagecontent =fields.get('message')
        #         message = ""
        #         message += "<html><body>"
        #         message += " <h2> Okay, how about this: </h2>"
        #         message += "<h1> %s </h1>" % messagecontent[0].decode('utf-8')
        #         message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
        #         message += "</body></html>"
        #     self.wfile.write(message.encode())
        # except:
        #     pass


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
