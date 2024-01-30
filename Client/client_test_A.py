# Importing necessary libraries
import json
import os
import requests
from bson import json_util
from datetime import datetime
import pytz

# Constants for server URLs
SERVER_URL = "http://127.0.0.1:61000"

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

    print(response.json())
    return response.status_code

# Function to change the username
def change_username(current_username, new_username):
    response = requests.post(f"{SERVER_URL}/change_username", json={"current_username": current_username, "new_username": new_username})
    return response.json()

# Function to change the password
def change_password(username, new_password):
    response = requests.post(f"{SERVER_URL}/change_password", json={"username": username, "new_password": new_password})
    return response.json()

# Function to send a message in an existing conversation
def send_message(sender, receiver, message, timestamp):
    response = requests.post(f"{SERVER_URL}/send_message", json={"sender": sender, "receiver": receiver, "message": message, "timestamp": timestamp})
    
    filename = f"MessagesDe_"+sender+"/"+receiver+".json"

    formatted_message = '{"message": "' + message + '", "receiver": "' + receiver + '", "sender": "' + sender + '", "timestamp": "' + timestamp + '"}'
    
    # Check if the "Messages" directory exists
    if not os.path.exists("MessagesDe_"+sender):
        # Create the "Messages" directory
        os.makedirs("MessagesDe_"+sender)

    if not os.path.exists(filename):
        with open(filename, 'w') as file:  # Ouverture en mode append
            file.write("")
    
    with open(filename, 'a') as file:  # Ouverture en mode write
        file.write(formatted_message)
        file.write("\n")

    
    return response.json()


def import_messages(receiver):

    if not os.path.exists("MessagesDe_"+receiver):
        os.makedirs("MessagesDe_"+receiver)
    
    response = requests.post(f"{SERVER_URL}/synchronize", json={"receiver": receiver})

    if response.status_code == 200:
        messages = json.loads(response.content.decode('utf-8'))  # Décoder la réponse JSON

        for message in messages:
            sender = message.get('sender')
            filename = f"MessagesDe_"+receiver+"/"+sender+".json"

            # Lecture du fichier existant ou création d'un nouveau fichier
            if not os.path.exists(filename):
                with open(filename, 'w') as file:  # Ouverture en mode append
                    file.write("")
            
            with open(filename, 'a') as file:  # Ouverture en mode write
                json.dump(message, file)
                file.write("\n")

    else:
        print(f"Erreur lors de la synchronisation des messages : {response.status_code}")


def display_messages(receiver):
    messages_dir = f"MessagesDe_{receiver}"

    # Check if the directory exists
    if not os.path.exists(messages_dir):
        print(f"No messages found for {receiver}")
        return

    # Read and display messages in JSON format
    for sender_file in os.listdir(messages_dir):
        filename = os.path.join(messages_dir, sender_file)
        try:
            with open(filename, 'r') as file:
                for line in file:
                    message_data = json.loads(line)
                    sender = message_data.get('sender')
                    receiver = message_data.get('receiver')
                    message_text = message_data.get('message')
                    timestamp = message_data.get('timestamp')
                    # Check if the message is for the specified receiver
                    if receiver == receiver:
                        print(f"From {sender} at {timestamp}: {message_text}")
        except json.JSONDecodeError as e:
            print(f"Error reading a message for {receiver}: {str(e)}")


def return_timestamp():
    # Get the current time in UTC
    utc_now = datetime.now(pytz.utc)

    # Format the timestamp as required
    formatted_timestamp = utc_now.strftime("%H:%M %d/%m/%Y")
    
    return formatted_timestamp

# Main client interface in the terminal
def main():
    while True:
        exit = False
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
                status = login(username, password)
                if status == 200:
                    auth_true = True
                else:
                    break

                while auth_true:
                    import_messages(username)
                    print("1. Create a new conversation")
                    print("2. See a conversation")
                    print("3. Modifiy username")
                    print("4. Modify password")
                    print("5. Exit")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        receiver = input("Enter receiver's username: ")

                        while True:
                            import_messages(username)
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

                        while True:
                            import_messages(username)
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

                        
                    elif choice == '3':
                        new_username = input("Enter new username: ")
                        response = change_username(username, new_username)
                        print(response)
                    
                    elif choice == '4':
                        new_password = input("Enter new password: ")
                        response = change_password(username, new_password)
                        print(response)
                        
                    elif choice == '5':
                        break

                    else:
                        print("Invalid choice. Please try again.")
                        
            elif choice == '3':
                exit = True
                break

            else:
                print("Invalid choice. Please try again.")
        
        if exit:
            break
        

# Uncomment the following line to run the client application (for deployment/testing)
main()


