#Python webserver

##Issue. Webserver.py can serve static html pages, and can call database functions from database_connection.py. BUT, as of right now, the html can't be changed by this webserver.py. That's why something like angular js is so useful. Apparently flask is similar for python. I might be able to call database_connection from inside html files. That might be a work around. BUt I don't know if html supports python

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from os import curdir, sep

from database_connection.py import testFunc()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                test = open('index.html')
                self.wfile.write(test.read().encode())
                return
            if self.path == '/restaurants':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                test = open('restaurants.html')
                self.wfile.write(test.read().encode())
                return
            if self.path == '/restaurants/new':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                test = open('new_restaurants.html')
                self.wfile.write(test.read().encode())
                return
            if self.path == '/restaurant/id/edit':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                test = open('edit_restaurant.html')
                self.wfile.write(test.read().encode())
                return
            if self.path == '/test':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                test = open('edit_restaurant.html')
                self.wfile.write(test.read().encode())
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
