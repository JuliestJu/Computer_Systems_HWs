import socket
import json
from datetime import datetime
from pymongo import MongoClient

def start_socket_server():
    # MongoDB setup
    client = MongoClient('mongodb://mongodb:27017/')
    db = client['messages_db']
    collection = db['messages']

    # Set up the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5001))
    server_socket.listen(5)

    print("Socket server listening on port 5001", flush=True)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}", flush=True)

        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received data: {data}", flush=True)
        if data:
            try:
                message_data = json.loads(data)
                message_data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                print(message_data, flush=True)
                collection.insert_one(message_data)
                client_socket.sendall(b"Data received and saved")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                client_socket.sendall(b"Invalid JSON data")
        
        client_socket.close()

if __name__ == '__main__':
    start_socket_server()
