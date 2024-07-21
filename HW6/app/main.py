import http.server
import socketserver
import os
from urllib.parse import urlparse, unquote
import json
import socket
import multiprocessing
from socket_server import start_socket_server

PORT = 3000
SOCKET_SERVER_HOST = 'socket-server'
SOCKET_SERVER_PORT = 5001

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        print(f"Requested path: {parsed_path.path}", flush=True)
        if parsed_path.path == '/':
            self.path = '/templates/index.html'
        elif parsed_path.path == '/message':
            self.path = '/templates/message.html'
        elif parsed_path.path.startswith('/static'):
            self.path = parsed_path.path
        else:
            self.path = '/templates/error.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = {k: v for k, v in [qc.split("=") for qc in post_data.decode().split("&")]}
            
            # Send data to socket server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((SOCKET_SERVER_HOST, SOCKET_SERVER_PORT))
                sock.sendall(json.dumps(data).encode('utf-8'))
                response = sock.recv(1024)
                print(f"Response from socket server: {response.decode('utf-8')}", flush=True)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Message sent successfully")

    def log_message(self, format, *args):
        return

def run_http_server():
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, MyHTTPRequestHandler)
    print(f'Serving HTTP on port {PORT}', flush=True)
    httpd.serve_forever()

if __name__ == '__main__':
    http_server_process = multiprocessing.Process(target=run_http_server)
    socket_server_process = multiprocessing.Process(target=start_socket_server)  # Call the socket server function

    http_server_process.start()
    socket_server_process.start()

    http_server_process.join()
    socket_server_process.join()
