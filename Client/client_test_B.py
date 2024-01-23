# Importing necessary libraries
import requests
import json

# Constants for server URLs (assuming localhost and default Flask port)
SERVER_URL = "http://127.0.0.1:5000"

# Function to register a new user
def register(username, password):
    response = requests.post(f"{SERVER_URL}/register", json={"username": username, "password": password})
    return response.json()

# Function for user login
def login(username, password):
    response = requests.post(f"{SERVER_URL}/login", json={"username": username, "password": password})
    return response.json()

# Function to create a new conversation
def create_conversation(sender, receiver, message):
    response = requests.post(f"{SERVER_URL}/conversation", json={"sender": sender, "receiver": receiver, "message": message})
    return response.json()

# Function to send a message in an existing conversation
def send_message(conversation_id, sender, message):
    response = requests.post(f"{SERVER_URL}/conversation/{conversation_id}", json={"sender": sender, "message": message})
    return response.json()

# Main client interface in the terminal
def main():
    while True:
        print("\nMessaging App Client")
        print("1. Register")
        print("2. Login")
        print("3. Create Conversation")
        print("4. Send Message")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(register(username, password))
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(login(username, password))
        elif choice == '3':
            sender = input("Enter your username: ")
            receiver = input("Enter receiver's username: ")
            message = input("Enter message: ")
            print(create_conversation(sender, receiver, message))
        elif choice == '4':
            conversation_id = input("Enter conversation ID: ")
            sender = input("Enter your username: ")
            message = input("Enter message: ")
            print(send_message(conversation_id, sender, message))
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

# Uncomment the following line to run the client application (for deployment/testing)
# main()

# Note: This is a simple CLI-based client. For production, error handling and input validation should be added.

