import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import urllib.parse as urlparse
from urllib.parse import parse_qs
import socket

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/templates/index.html"
        elif self.path == "/message.html":
            self.path = "/templates/message.html"
        elif self.path == "/style.css":
            self.path = "/static/style.css"
        elif self.path == "/logo.png":
            self.path = "/static/logo.png"
        else:
            self.path = "/templates/error.html"
            self.send_response(404)
        return super().do_GET()

    def do_POST(self):
        if self.path == "/message":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = parse_qs(post_data.decode('utf-8'))

            message_data = {
                "username": parsed_data["username"][0],
                "message": parsed_data["message"][0]
            }
            
            # Send data to socket server
            self.send_to_socket_server(message_data)
            
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def send_to_socket_server(self, data):
        server_address = ('localhost', 5001)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(server_address)
            sock.sendall(str(data).encode('utf-8'))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def run(server_class=ThreadedHTTPServer, handler_class=CustomHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
