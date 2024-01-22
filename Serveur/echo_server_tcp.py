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
sqlite_cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, sender TEXT, receiver TEXT, message TEXT)')

class Server:
    def __init__(self):
        pass

    def authenticate_user(self, username, password):
        user = users_collection.find_one({'username': username})
        if user and user['password'] == password:
            return True
        return False

    def save_message(self, sender, receiver, message):
        sqlite_cursor.execute('INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)', (sender, receiver, message))
        sqlite_conn.commit()

    def get_messages(self, user):
        with sqlite3.connect('messages.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT sender, message FROM messages WHERE receiver = ?', (user,))
            messages = cursor.fetchall()
        return messages
    

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

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')
    server.save_message(sender, receiver, message)
    return jsonify({'message': 'Message sent successfully'}), 200

@app.route('/get_messages/<user>', methods=['GET'])
def get_messages(user):
    messages = server.get_messages(user)
    messages_dict_list = [{'sender': msg[0], 'message': msg[1]} for msg in messages]
    return jsonify(messages_dict_list), 200

if __name__ == '__main__':
    app.run(debug=True)
