# Importing necessary libraries
import json
import os
import requests
import yaml
from bson import json_util
from datetime import datetime
import pytz

# Constants for server URLs (assuming localhost and default Flask port)
SERVER_URL = "http://127.0.0.1:5000"

def welcome():
    response = requests.get(f'{SERVER_URL}/welcome')
    welcome_message = response.json()
    return welcome_message

# Function to register a new user
def register(username, password):
    response = requests.post(f"{SERVER_URL}/register", json={"username": username, "password": password})
    return response.json()

def verify_username(username):
    response = requests.post(f"{SERVER_URL}/verify_username", json={"username": username})
    return response.json()

# Function for user login
def login(username, password):
    response = requests.post(f"{SERVER_URL}/login", json={"username": username, "password": password})
    return response.json()


# Function to send a message in an existing conversation
def send_message(sender, receiver, message, timestamp):
    response = requests.post(f"{SERVER_URL}/send_message", json={"sender": sender, "receiver": receiver, "message": message, "timestamp": timestamp})
    return response.json()

def import_messages(receiver):
    if not os.path.exists("Messages"):
        os.makedirs("Messages")
    
    response = requests.post(f"{SERVER_URL}/synchronize", json={"receiver": receiver})

    if response.status_code == 200:
        messages = json.loads(response.content.decode('utf-8'))  # Décoder la réponse JSON

        for message in messages:
            sender = message.get('sender')
            filename = f"Messages/{sender}.yaml"

            # Conversion du message MongoDB en format JSON
            message_json = json.dumps(message)

            # Lecture du fichier existant ou création d'un nouveau fichier
            if not os.path.exists(filename):
                with open(filename, 'w') as file:  # Ouverture en mode append
                    file.write("---\n")
            
            with open(filename, 'a') as file:  # Ouverture en mode write
                yaml.dump(message_json, file)
                file.write("---\n")
    else:
        print(f"Erreur lors de la synchronisation des messages : {response.status_code}")

def display_messages(receiver):
    filename = f"Messages/{receiver}.yaml"

    # Vérifier si le fichier existe
    if not os.path.exists(filename):
        print(f"No messages found for {receiver}")
        return

    # Lire le contenu du fichier YAML
    with open(filename, 'r') as file:
        try:
            yaml_documents = file.read().split("---\n")

            # Parcourir chaque document YAML
            for yaml_doc in yaml_documents:
                if yaml_doc.strip():  # Ignorer les documents vides
                    message_data = json.loads(yaml_doc)
                    sender = message_data.get('sender')
                    message_text = message_data.get('message')
                    timestamp = message_data.get('timestamp')
                    print(f"De {sender} à {timestamp}: {message_text}")
        except Exception as e:
            print(f"Error reading messages for {receiver}: {str(e)}")

def return_timestamp():
    # Get the current time in UTC
    utc_now = datetime.now(pytz.utc)

    # Format the timestamp as required
    formatted_timestamp = utc_now.strftime("%H:%M %d/%m/%Y")
    
    return formatted_timestamp

# Main client interface in the terminal
def main():
    while True:
        print(welcome())

        while True:
            print("\nMessaging App Client")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")
                print(register(username, password))
            elif choice == '2':
                username = input("Enter username: ")
                password = input("Enter password: ")
                print(login(username, password))
                
                while True:
                    import_messages(username)
                    print("1. Create a new conversation")
                    print("2. See a conversation")
                    print("3. Exit")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        receiver = input("Enter receiver's username: ")

                        while True:
                            if verify_username(receiver):
                                print("1. Send a message to " + receiver)
                                print("2. Exit")
                                choice = input("Enter your choice: ")

                                if choice == '1':
                                    message = input("Enter message: ")
                                    print(send_message(username, receiver, message, return_timestamp()))

                                elif choice == '2':
                                    break

                                else:
                                    print("Invalid choice. Please try again.")
                            
                            else:
                                print("This username does not exists")
                                break


                    elif choice == '2':
                        receiver = input("Enter receiver's username: ")
                        display_messages(receiver)
                        

                    elif choice == '3':
                        break

                    else:
                        print("Invalid choice. Please try again.")
                        
            elif choice == '3':
                break

            else:
                print("Invalid choice. Please try again.")

# Uncomment the following line to run the client application (for deployment/testing)
main()

# Note: This is a simple CLI-based client. For production, error handling and input validation should be added.

