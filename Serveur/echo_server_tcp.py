import datetime

from flask import Flask, request, jsonify
from pymongo import MongoClient
import sqlite3

app = Flask(__name__)

# Configuration MongoDB pour l'authentification
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['authentication_db']
users_collection = db['users']

# Configuration SQLite pour le stockage des messages
sqlite_conn = sqlite3.connect('messages.db', check_same_thread=False)
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute('CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)')
sqlite_cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, conversation_id INTEGER, sender TEXT, receiver TEXT, message TEXT, sent_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (conversation_id) REFERENCES conversations(id))')

class Server:
    def __init__(self):
        pass

    def authenticate_user(self, username, password):
        user = users_collection.find_one({'username': username})
        if user and user['password'] == password:
            return True
        return False

    def create_conversation(self, participants):
        conversation = {'participants': participants, 'created_at': datetime.now()}
        return db['conversations'].insert_one(conversation).inserted_id

    def save_message(self, conversation_id, sender, receiver, message):
            message_data = {
                'conversation_id': ObjectId(conversation_id),
                'sender': sender,
                'receiver': receiver,
                'message': message,
                'sent_at': datetime.now()
            }
            db['messages'].insert_one(message_data)

    def get_messages(self, user):
        conversations = db['conversations'].find({'participants': user})
        conversation_ids = [conv['_id'] for conv in conversations]
        messages = db['messages'].find({'conversation_id': {'$in': conversation_ids}})
        return [{'sender': msg['sender'], 'message': msg['message']} for msg in messages]
    

server = Server()


@app.route('/welcome', methods=['GET'])
def welcome():
    welcome_message = {
        'message': 'Bienvenue sur le service de messagerie instantanée.',
        'options': [
            '1. S\'authentifier',
            '2. Créer un compte'
        ]
    }
    return jsonify(welcome_message), 200

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Vérifier si l'utilisateur existe déjà
    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409

    # Ajouter le nouvel utilisateur
    users_collection.insert_one({'username': username, 'password': password})
    return jsonify({'message': 'Account created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if server.authenticate_user(username, password):
        return jsonify({'message': 'Authentication successful'}), 200
    else:
        return jsonify({'message': 'Authentication failed'}), 401

@app.route('/create_conversation', methods=['POST'])
def create_conversation():
    participants = request.json.get('participants')
    conversation_id = server.create_conversation(participants)
    return jsonify({'conversation_id': str(conversation_id)}), 201


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    conversation_id = data.get('conversation_id')
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')
    server.save_message(conversation_id, sender, receiver, message)
    return jsonify({'message': 'Message sent successfully'}), 200

@app.route('/get_messages/<user>', methods=['GET'])
def get_messages(user):
    messages = server.get_messages(user)
    messages_dict_list = [{'sender': msg[0], 'message': msg[1]} for msg in messages]
    return jsonify(messages_dict_list), 200

if __name__ == '__main__':
    app.run(debug=True)
