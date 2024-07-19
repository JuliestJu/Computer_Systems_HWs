import socket
import json
from datetime import datetime
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://mongodb:27017/')
db = client['messages_db']
collection = db['messages']

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen(5)

print("Socket server listening on port 5000")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    data = client_socket.recv(1024).decode('utf-8')
    print(f"Received data: {data}")  # Log received data
    if data:
        try:
            # Convert received data to dictionary and save to MongoDB
            message_data = json.loads(data)
            message_data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            collection.insert_one(message_data)
            client_socket.sendall(b"Data received and saved")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")  # Log JSON decode error
            client_socket.sendall(b"Invalid JSON data")
    
    client_socket.close()
