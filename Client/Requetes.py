# Contient toutes les requêtes susceptibles d'être envoyé par le client

import base64
import json
import os
import time
import requests

# Adresse du serveur
SERVER_URL = "http://127.0.0.1:61000"

# Crée un utilisateur
def creationCompte(pseudo, mdp):
    retour = requests.post(f"{SERVER_URL}/creationCompte", json={"pseudo": pseudo, "mdp": mdp})
    return retour.json()

# Vérifier que l'utilisateur existe
def verificationUtilisateur(pseudo):
    retour = requests.post(f"{SERVER_URL}/verificationUtilisateur", json={"pseudo": pseudo})
    return retour.json()


# Se Connecter
def seConnecter(pseudo, mdp):
    retour = requests.post(f"{SERVER_URL}/seConnecter", json={"pseudo": pseudo, "mdp": mdp})

    print(retour.json())
    return retour.status_code


# Changer le pseudo
def changer_pseudo(pseudo_actuel, new_pseudo):
    retour = requests.post(f"{SERVER_URL}/changer_pseudo",
                           json={"current_username": pseudo_actuel, "new_username": new_pseudo})
    return retour.json()


# Changer le mot de passe
def changer_mdp(pseudo, new_mdp):
    retour = requests.post(f"{SERVER_URL}/changer_mdp", json={"pseudo": pseudo, "new_mdp": new_mdp})
    return retour.json()


# Function to send a message in an existing conversation
def envoyer_message(sender, receiver, message, timestamp):
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
def envoyer_fichier(sender, receiver, filename, file_data, timestamp):
    
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


def import_periodically(receiver):
    while True:
        import_messages(receiver)
        import_files(receiver)
        # Sleep for 5 seconds before running again
        time.sleep(5)


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

