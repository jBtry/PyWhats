import socket
from _thread import *
import pymongo
from datetime import datetime

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
clients = {}  # Dictionnaire pour stocker les connexions des clients

# Il me manque encore à tout mettre en méthodes

# Avoir la base de donnée
def get_database():

    DATABASE_URL = "mongodb://localhost:27017/"
    DATABASE_NAME = "database_pywhats"

    serverDB = pymongo.MongoClient(DATABASE_URL)
    return serverDB[DATABASE_NAME]

# Enregistre dans une collection un message (item)
def save_messages_database(collection, item):
    collection.insert_one(item)

# Retourne les messages qui correspondent à l'émetteur et au destinataire dans une collection 
def read_messages_database(collection, sender, receiver):
    # création de la requête pour trouver les messages
    query = {
        'client_address': sender,
        'recipient': receiver
    }
    return collection.find(query)

# Supprime un message (item) d'une collection'
def delete_messages_database(collection, item):
    collection.drop(item)

# Envoie des messages à des utilisateurs destinataires
def send_messages():
    return 

# Reçoit des messages des utilisateurs émetteurs
def receive_messages():
    return

# Quand un utilisateur se connecte, il y a une synchronisation où il va recevoir tout les messages qui
# lui ont été envoyé alors qu'il n'était pas connecté au serveur
def synchronization():
    return

# Vérifie dans la base de donnée si le username et le password corresponde bien à un document
# pour l'authentification de l'utilisateur
def verify_authentification(username_auth, password_auth):
    dbname = get_database
    result = dbname.dictionnary.count_document({
        '$and': [
            {'username': username_auth},
            {'password': password_auth}
        ]
    })
    while result:
        user_authenticated = True
        return user_authenticated

    user_authenticated = False
    return user_authenticated


# Faire le reste en méthode

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
        
        # item_1 = [timestamp, client_address, recipient, message]

        # document = {
        #     'timestamp': item_1[0],
        #     'sender': item_1[1],
        #     'recipient': item_1[2],
        #     'message': item_1[3]
        # }

        # messages_collection.insert_one(document)

        # test_message = messages_collection.find()

        # for test_message in message:
        #     print(f"Timestamp: {message['timestamp']}")
        #     print(f"Sender: {message['sender']}")
        #     print(f"Recipient: {message['recipient']}")
        #     print(f"Message: {message['message']}")

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