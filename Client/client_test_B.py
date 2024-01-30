# Importing necessary libraries
import base64
import json
import os
import threading
import time
import requests
import yaml
from bson import json_util
from datetime import datetime
import pytz

# Constants for server URLs (assuming localhost and default Flask port)
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


# Function to send a message in an existing conversation
def send_file(sender, receiver, filename, file_data, timestamp):
    
    file_data_base64 = base64.b64encode(file_data).decode('utf-8')

    response = requests.post(f"{SERVER_URL}/send_file", json={"sender": sender, "receiver": receiver, "filename": filename, "file_data": file_data_base64, "timestamp": timestamp})
    
    pathname = f"FichiersDe_"+sender+"/"+receiver+".json"

    formatted_message = {
        "filename": filename,
        "file_data": file_data_base64,
        "receiver": receiver,
        "sender": sender,
        "timestamp": timestamp
    }    

    # Check if the directory exists
    if not os.path.exists("FichiersDe_"+sender):
        # Create the directory
        os.makedirs("FichiersDe_"+sender)

    if not os.path.exists(pathname):
        with open(pathname, 'w') as file:  # Ouverture en mode append
            file.write("")
    
    with open(pathname, 'a') as file:  # Ouverture en mode write
        json.dump(formatted_message, file)
        file.write("\n")

 
    if response.status_code == 200:
        # Vérifier si la réponse contient des données JSON valides
        try:
            response_json = response.json()
            return response_json
        except json.JSONDecodeError as e:
            print(f"Erreur lors de la décodage de la réponse JSON : {e}")
            return {"error": "Erreur lors du décodage de la réponse JSON"}
    else:
        print(f"La requête a échoué avec le code d'état : {response.status_code}")
        return {"error": f"La requête a échoué avec le code d'état : {response.status_code}"}


def import_messages(receiver):

    if not os.path.exists("MessagesDe_"+receiver):
        os.makedirs("MessagesDe_"+receiver)
    
    response = requests.post(f"{SERVER_URL}/synchronize", json={"receiver": receiver})

    if response.status_code == 200:
        messages = json.loads(response.content.decode('utf-8'))  # Décoder la réponse JSON

        if messages != []:
            cpt = 0
            sender_notif = ""
            for message in messages:
                sender = message.get('sender')
                filename = f"MessagesDe_"+receiver+"/"+sender+".json"

                # Lecture du fichier existant ou création d'un nouveau fichier
                if not os.path.exists(filename):
                    with open(filename, 'w') as file:  # Ouverture en mode write
                        file.write("")
                
                with open(filename, 'a') as file:  # Ouverture en mode append
                    json.dump(message, file)
                    file.write("\n")
                
                sender_notif = sender
                cpt = cpt + 1

            print(f"\n                                              You received {cpt} message from {sender_notif}")
                

    else:
        print(f"Erreur lors de la synchronisation des messages : {response.status_code}")


def import_files(receiver):
    if not os.path.exists("FichiersDe_" + receiver):
        os.makedirs("FichiersDe_" + receiver)

    response = requests.post(f"{SERVER_URL}/synchronize_files", json={"receiver": receiver})

    if response.status_code == 200:
        files = json.loads(response.content.decode('utf-8'))  # Decode the JSON response

        if files != []:
            sender_notif = ""
            filename_notif = ""

            for file_info in files:
                sender = file_info.get('sender')
                filename = file_info.get('filename')
                file_data_base64 = file_info.get('file_data')

                # Decode the base64 file data
                file_data = base64.b64decode(file_data_base64)

                # Save the file to the receiver's directory
                file_path = f"FichiersDe_{receiver}/{filename}"
                with open(file_path, 'wb') as file:
                    file.write(file_data)
                
                sender_notif = sender
                filename_notif = filename

            print(f"\n                                              Received file '{filename_notif}' from {sender_notif}")

    else:
        print(f"Error synchronizing files: {response.status_code}")


def display_messages(username, receiver):
    messages_dir = f"MessagesDe_{username}/{receiver}.json"

    # Check if the directory exists
    if not os.path.exists(messages_dir):
        print(f"No messages found for {receiver}")
        return

    # Ouvrir le fichier JSON et lire son contenu ligne par ligne
    with open(messages_dir, 'r') as file:
        lines = file.readlines()

    # Parcourir chaque ligne (chaque message) et l'afficher dans le format souhaité
    for line in lines:
        message = json.loads(line)
        sender = message.get('sender')
        timestamp = message.get('timestamp')
        message_text = message.get('message')

        print(f"From {sender} at {timestamp}: {message_text}")


# Fonction pour supprimer une conversation
def delete_conversation(username, receiver):
    # Chemin du fichier JSON de la conversation
    filepath = f"MessagesDe_{username}/{receiver}.json"

    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Conversation with {receiver} has been deleted.")
    else:
        print(f"No conversation found with {receiver}.")


def return_timestamp():
    # Get the current time in UTC
    utc_now = datetime.now(pytz.utc)

    # Format the timestamp as required
    formatted_timestamp = utc_now.strftime("%H:%M %d/%m/%Y")
    
    return formatted_timestamp

def import_periodically(receiver):
    while True:
        import_messages(receiver)
        import_files(receiver)
        # Sleep for 5 seconds before running again
        time.sleep(5)

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
                    import_messages_thread = threading.Thread(target=import_periodically, args=(username,))
                    import_messages_thread.daemon = True
                    import_messages_thread.start()
                else:
                    break

                while auth_true:
                    time.sleep(1)
                    print("1. Envoyer un message")
                    print("2. Envoyer un fichier")
                    print("3. Gérer son profil")
                    print("4. Supprimer une conversation")
                    print("5. Se déconnecter")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        print("1. Saisir le destinataire")
                        print("2. Retour")
                        choice = input("Enter your choice: ")
                        
                        if choice == '1':
                            receiver = input("Enter receiver's username: ")
                            

                            while verify_username(receiver):
                                display_messages(username, receiver)

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
                            

                    elif choice == '2':

                        print("1. Saisir le destinataire")
                        print("2. Retour")
                        choice = input("Enter your choice: ")

                        if choice == '1':

                            receiver = input("Enter receiver's username: ")
                            while verify_username(receiver):

                                print("1. Send a file to " + receiver)
                                print("2. Exit")
                                choice = input("Enter your choice: ")

                                if choice == '1':

                                    file_path = input("Enter the path to the file you want to send: ")
                                    
                                    if os.path.exists(file_path):
                                        with open(file_path, 'rb') as file:
                                            file_data = file.read()

                                        filename = os.path.basename(file_path)
                                        print(send_file(username, receiver, filename, file_data, return_timestamp()))

                                        time.sleep(5)
                                    else:
                                        print("File not found. Please enter a valid file path.")
                                
                                elif choice == '2':
                                    break

                                else:
                                    print("Invalid choice. Please try again.")

                        
                    elif choice == '3':
                        while True:
                            print("1. Modifier pseudo")
                            print("2. Modifier mot de passe")
                            print("3. Exit")
                            choice = input("Enter your choice: ")

                            if choice =='1':
                                new_username = input("Enter new username: ")
                                response = change_username(username, new_username)
                                print(response)
                            
                            elif choice =='2':
                                new_password = input("Enter new password: ")
                                response = change_password(username, new_password)
                                print(response)

                            elif choice =='3':
                                break

                            else:
                                print("Invalid choice. Please try again.")
                        
                    elif choice == '4':
                        print("1. Saisir le destinataire")
                        print("2. Retour")
                        choice = input("Enter your choice: ")
                        
                        if choice == '1':
                            receiver = input("Enter receiver's username: ")
                            verify_username(receiver)

                            display_messages(receiver)
                            print("1. Supprimer cette conversation ?")
                            print("2. Exit")
                            choice = input("Enter your choice: ")

                            if choice == '1':
                                print(delete_conversation(username, receiver))

                            elif choice == '2':
                                break

                            else:
                                print("Invalid choice. Please try again.")

                        

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