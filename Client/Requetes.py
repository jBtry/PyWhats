# Contient toutes les requêtes susceptibles d'être envoyé par le client

import json
import os
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


# Envoyer un message dans une conversation existante
def envoyer_message(envoyeur, destinataire, message, timestamp):
    retour = requests.post(f"{SERVER_URL}/envoyer_message",
                           json={"envoyeur": envoyeur, "destinataire": destinataire, "message": message, "timestamp": timestamp})

    filename = f"MessagesDe_" + envoyeur + "/" + destinataire + ".json"

    formatted_message = '{"message": "' + message + '", "receiver": "' + destinataire + '", "sender": "' + envoyeur + '", "timestamp": "' + timestamp + '"}'

    # Check if the "Messages" directory exists
    if not os.path.exists("MessagesDe_" + envoyeur):
        # Create the "Messages" directory
        os.makedirs("MessagesDe_" + envoyeur)

    if not os.path.exists(filename):
        with open(filename, 'w') as file:  # Ouverture en mode append
            file.write("")

    with open(filename, 'a') as file:  # Ouverture en mode write
        file.write(formatted_message)
        file.write("\n")

    return retour.json()


def import_messages(destinataire):
    if not os.path.exists("MessagesDe_" + destinataire):
        os.makedirs("MessagesDe_" + destinataire)

    retour = requests.post(f"{SERVER_URL}/synchroniser", json={"destinataire": destinataire})

    if retour.status_code == 200:
        messages = json.loads(retour.content.decode('utf-8'))  # Décoder la réponse JSON

        for message in messages:
            envoyeur = message.get('destinataire')
            filename = f"MessagesDe_" + destinataire + "/" + envoyeur + ".json"

            # Lecture du fichier existant ou création d'un nouveau fichier
            if not os.path.exists(filename):
                with open(filename, 'w') as file:  # Ouverture en mode append
                    file.write("")

            with open(filename, 'a') as file:  # Ouverture en mode write
                json.dump(message, file)
                file.write("\n")

    else:
        print(f"Erreur lors de la synchronisation des messages : {retour.status_code}")


def display_messages(destinataire):
    messages_dir = f"MessagesDe_{destinataire}"

    # Check if the directory exists
    if not os.path.exists(messages_dir):
        print(f"No messages found for {destinataire}")
        return

    # Read and display messages in JSON format
    for sender_file in os.listdir(messages_dir):
        filename = os.path.join(messages_dir, sender_file)
        try:
            with open(filename, 'r') as file:
                for line in file:
                    message_data = json.loads(line)
                    sender = message_data.get('sender')
                    destinataire = message_data.get('receiver')
                    message_text = message_data.get('message')
                    timestamp = message_data.get('timestamp')
                    # Check if the message is for the specified receiver
                    if destinataire == destinataire:
                        print(f"From {sender} at {timestamp}: {message_text}")
        except json.JSONDecodeError as e:
            print(f"Error reading a message for {destinataire}: {str(e)}")


