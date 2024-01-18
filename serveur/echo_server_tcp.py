import socket
from _thread import *
import pymongo
from datetime import datetime

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
clients = {}  # Dictionnaire pour stocker les connexions des clients

DATABASE_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "database_pywhats"

serverDB = pymongo.MongoClient(DATABASE_URL)
database = serverDB[DATABASE_NAME]

messages_collection = database['messages']


try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection, client_address):
    connection.send(str.encode('Welcome to the Server'))
    
    while True:
        data = connection.recv(2048)
        if not data:
            break
        
        # Enregistrement du message avec le timestamp dans la collection MongoDB
        timestamp = datetime.utcnow()  # Obtient le timestamp actuel en format UTC

        # Assume the data received is in the format "recipient: message"
        recipient, message = data.decode('utf-8').split(':', 1)
        
        # Enregistrement du message dans la collection MongoDB
        
        item_1 = [timestamp, client_address, recipient, message]

        document = {
            'timestamp': item_1[0],
            'sender': item_1[1],
            'recipient': item_1[2],
            'message': item_1[3]
        }

        messages_collection.insert_one(document)

        test_message = messages_collection.find()

        for test_message in message:
            print(f"Timestamp: {message['timestamp']}")
            print(f"Sender: {message['sender']}")
            print(f"Recipient: {message['recipient']}")
            print(f"Message: {message['message']}")

        # Check if the recipient is a valid connected client
        if recipient in clients:
            recipient_conn = clients[recipient]
            recipient_conn.sendall(str.encode(f'Message from {client_address}: {message}'))
        else:
            connection.sendall(str.encode('Recipient not found or not connected'))
    
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))

    client_name = Client.recv(1024).decode('utf-8')
    clients[client_name] = Client

    start_new_thread(threaded_client, (Client, address))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSocket.close()