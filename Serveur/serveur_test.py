# Importing necessary libraries
from flask import Flask, request, jsonify
import sqlite3
from pymongo import MongoClient
import bcrypt

# Initializing Flask app
app = Flask(__name__)

# Setting up MongoDB client (assuming MongoDB is running on the default port)
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['messaging_app']  # Database name: messaging_app
messages_collection = mongo_db['conversations']  # Collection for conversations

# Function to connect to SQLite database for user authentication
def get_sqlite_connection():
    conn = sqlite3.connect('users.db')
    return conn

# Function to create users table in SQLite (to be run once)
def create_users_table():
    conn = get_sqlite_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (username TEXT PRIMARY KEY NOT NULL,
                     password TEXT NOT NULL);''')
    conn.commit()
    conn.close()

# Function to hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to verify password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)


@app.route('/welcome', methods=['GET'])
def welcome():
    welcome_message = {
        'message': 'Bienvenue sur le service de messagerie instantanée.',
    }
    return jsonify(welcome_message), 200

# Flask route for user registration
@app.route('/register', methods=['POST'])
def register():
    # Extracting username and password from request
    username = request.json['username']
    password = request.json['password']

    # Hashing the password
    hashed_password = hash_password(password)

    # Inserting user into SQLite database
    conn = get_sqlite_connection()
    try:
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                     (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username already exists'}), 400
    finally:
        conn.close()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/verify_username', methods=['POST'])
def verify_username():
    # Récupérer le nom d'utilisateur à partir de la requête
    username = request.json['username']

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Requête pour vérifier l'existence du nom d'utilisateur
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()

    # Vérifier si le nom d'utilisateur a été trouvé
    if user:
        return jsonify(True), 200
    else:
        return jsonify(False), 200


# Flask route for user login
@app.route('/login', methods=['POST'])
def login():
    # Extracting username and password from request
    username = request.json['username']
    password = request.json['password']

    # Retrieving user from SQLite database
    conn = get_sqlite_connection()
    cursor = conn.execute('SELECT password FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()

    # Verifying password
    if user and verify_password(user[0], password):
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/change_username', methods=['POST'])
def change_username():
    current_username = request.json['current-username']
    new_username = request.json['new_password']

    already_exist = verify_username(new_username)

    if already_exist:
        return jsonify({'message': 'Username already exists'}), 400
    else:
        # Inserting user into SQLite database
        conn = get_sqlite_connection()
        try:
            conn.execute('UPDATE users SET username =? WHERE username =?', 
                        (new_username, current_username))
            conn.commit()
        except sqlite3.IntegrityError:
            return jsonify({'message': 'Error updating the username'}), 400
        finally:
            conn.close()

        return jsonify({'message': 'Username changed successfully'}), 201


@app.route('/change_password', methods=['POST'])
def change_password():

    username = request.json['username']
    new_password = request.json['new_password']

    hashed_password = hash_password(new_password)
    # Inserting user into SQLite database
    conn = get_sqlite_connection()
    try:
        conn.execute('UPDATE users SET password =? WHERE username =?', 
                    (hashed_password, username))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Error updating the password'}), 400
    finally:
        conn.close()

    return jsonify({'message': 'Password changed successfully'}), 201


# Flask route for sending a message
@app.route('/send_message', methods=['POST'])
def send_message():
    # Extracting sender and message from request
    sender = request.json['sender']
    receiver = request.json['receiver']
    message_text = request.json['message']
    timestamp = request.json['timestamp']

    message = {
    'sender': sender,
    'receiver': receiver,
    'message': message_text,
    'timestamp': timestamp
    }

    # Adding message to an existing conversation in MongoDB
    messages_collection.insert_one(message)

    return jsonify({'message': 'Message sent successfully'}), 200

@app.route('/synchronize', methods=['POST'])
def synchronize():
    # Extracting sender and message from request
    receiver = request.json['receiver']

    messages = messages_collection.find({'receiver': receiver})

    synchronized_messages = []

    # Ajouter chaque message à la liste synchronisée
    for message in messages:
        synchronized_messages.append({
            'sender': message['sender'],
            'receiver': message['receiver'],
            'message': message['message'],
            'timestamp': message['timestamp']
        })
    
    criteria = {'receiver': receiver}
    deleted_result = messages_collection.delete_many(criteria)
    print(f"Number of messages deleted: {deleted_result.deleted_count}")

    return jsonify(synchronized_messages), 200

if __name__ == '__main__':
    create_users_table()  # Créer la table des utilisateurs au démarrage
    app.run(host='0.0.0.0', port=61000, debug=True)
# Note: Additional error handling, input validation, and security measures (like API authentication) should be added in a production environment.

