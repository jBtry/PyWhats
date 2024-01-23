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
conversations_collection = mongo_db['conversations']  # Collection for conversations

# Function to connect to SQLite database for user authentication
def get_sqlite_connection():
    conn = sqlite3.connect('users.db')
    return conn

# Function to create users table in SQLite (to be run once)
def create_users_table():
    conn = get_sqlite_connection()
    conn.execute('''CREATE TABLE users 
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

# Flask route for creating a conversation
@app.route('/conversation', methods=['POST'])
def create_conversation():
    # Extracting sender, receiver, and message from request
    sender = request.json['sender']
    receiver = request.json['receiver']
    message = request.json['message']

    # Creating a new conversation in MongoDB
    conversation_id = conversations_collection.insert_one({
        'participants': [sender, receiver],
        'messages': [{'sender': sender, 'message': message}]
    }).inserted_id

    return jsonify({'message': 'Conversation created', 'conversation_id': str(conversation_id)}), 201

# Flask route for sending a message
@app.route('/conversation/<conversation_id>', methods=['POST'])
def send_message(conversation_id):
    # Extracting sender and message from request
    sender = request.json['sender']
    message = request.json['message']

    # Adding message to an existing conversation in MongoDB
    conversations_collection.update_one(
        {'_id': conversation_id},
        {'$push': {'messages': {'sender': sender, 'message': message}}}
    )

    return jsonify({'message': 'Message sent'}), 200

# Uncomment the following line to start the Flask app (for deployment/testing)
app.run(debug=True)

# Note: Additional error handling, input validation, and security measures (like API authentication) should be added in a production environment.

