import http.server
import socketserver
import os
from urllib.parse import urlparse, unquote

PORT = 3001

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self.path = '/templates/index.html'
        elif parsed_path.path == '/message':
            self.path = '/templates/message.html'
        elif parsed_path.path.startswith('/static'):
            self.path = parsed_path.path
        else:
            self.path = '/templates/error.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        return  # Suppress logging

def run(server_class=http.server.HTTPServer, handler_class=MyHTTPRequestHandler):
    os.chdir('app')  # Change working directory to app to serve files correctly
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f'Serving HTTP on port {PORT}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
