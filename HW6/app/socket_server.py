import socket
import json
from datetime import datetime
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['message_db']
collection = db['messages']

def save_to_db(data):
    data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    collection.insert_one(data)

def start_socket_server():
    server_address = ('localhost', 5001)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(1)
    
    print('Socket server listening on port 5001')
    
    while True:
        connection, client_address = sock.accept()
        try:
            data = connection.recv(1024)
            if data:
                message_data = json.loads(data.decode('utf-8').replace("'", '"'))
                save_to_db(message_data)
        finally:
            connection.close()

if __name__ == "__main__":
    start_socket_server()