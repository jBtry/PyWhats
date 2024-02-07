# Contient toutes les requêtes susceptibles d'être envoyé par le client

import base64
import json
import os
import time
import requests

from OutilsClient import *
from Texte import *

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
                           json={"pseudo_actuel": pseudo_actuel, "new_pseudo": new_pseudo})
    return retour.json()


# Changer le mot de passe
def changer_mdp(pseudo, new_mdp):
    if verificationMDP(new_mdp) :
        retour = requests.post(f"{SERVER_URL}/changer_mdp", json={"pseudo": pseudo, "new_mdp": new_mdp})
        return retour.json()
    else :
        print(MESSAGE_MDP_INVALIDE)


# Function to send a message in an existing conversation
def envoyer_message(envoyeur, destinataire, message, timestamp):
    response = requests.post(f"{SERVER_URL}/envoyer_message", json={"envoyeur": envoyeur, "destinataire": destinataire, "message": message, "timestamp": timestamp})
    
    filename = f"MessagesDe_"+envoyeur+"/"+destinataire+".json"

    formatted_message = '{"message": "' + message + '", "destinataire": "' + destinataire + '", "envoyeur": "' + envoyeur + '", "timestamp": "' + timestamp + '"}'
    
    # Check if the "Messages" directory exists
    if not os.path.exists("MessagesDe_"+envoyeur):
        # Create the "Messages" directory
        os.makedirs("MessagesDe_"+envoyeur)

    if not os.path.exists(filename):
        with open(filename, 'w') as file:  # Ouverture en mode append
            file.write("")
    
    with open(filename, 'a') as file:  # Ouverture en mode write
        file.write(formatted_message)
        file.write("\n")

    return response.json()

# Function to send a message in an existing conversation
def envoyer_fichier(envoyeur, destinataire, filename, file_data, timestamp):
    
    file_data_base64 = base64.b64encode(file_data).decode('utf-8')

    response = requests.post(f"{SERVER_URL}/envoyer_fichier", json={"envoyeur": envoyeur, "destinataire": destinataire, "filename": filename, "file_data": file_data_base64, "timestamp": timestamp})
     
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


def import_messages(destinataire):

    if not os.path.exists("MessagesDe_"+destinataire):
        os.makedirs("MessagesDe_"+destinataire)
    
    response = requests.post(f"{SERVER_URL}/synchroniser_messages", json={"destinataire": destinataire})

    if response.status_code == 200:
        messages = json.loads(response.content.decode('utf-8'))  # Décoder la réponse JSON

        if messages != []:
            cpt = 0
            envoyeur_notif = ""
            for message in messages:
                envoyeur = message.get('envoyeur')
                filename = f"MessagesDe_"+destinataire+"/"+envoyeur+".json"

                # Lecture du fichier existant ou création d'un nouveau fichier
                if not os.path.exists(filename):
                    with open(filename, 'w') as file:  # Ouverture en mode write
                        file.write("")
                
                with open(filename, 'a') as file:  # Ouverture en mode append
                    json.dump(message, file)
                    file.write("\n")
                
                envoyeur_notif = envoyeur
                cpt = cpt + 1

            print(f"\n                                                        Tu as reçu {cpt} message(s) de {envoyeur_notif}")
                

    else:
        print(f"Erreur lors de la synchronisation des messages : {response.status_code}")


def import_fichiers(destinataire):
    if not os.path.exists("FichiersDe_" + destinataire):
        os.makedirs("FichiersDe_" + destinataire)

    response = requests.post(f"{SERVER_URL}/synchroniser_fichiers", json={"destinataire": destinataire})

    if response.status_code == 200:
        files = json.loads(response.content.decode('utf-8'))  # Decode the JSON response

        if files != []:
            envoyeur_notif = ""
            filename_notif = ""

            for file_info in files:
                envoyeur = file_info.get('envoyeur')
                filename = file_info.get('filename')
                file_data_base64 = file_info.get('file_data')

                # Decode the base64 file data
                file_data = base64.b64decode(file_data_base64)

                # Save the file to the destinataire's directory
                file_path = f"FichiersDe_{destinataire}/{filename}"
                with open(file_path, 'wb') as file:
                    file.write(file_data)
                
                envoyeur_notif = envoyeur
                filename_notif = filename

            print(f"\n                                                        Fichier '{filename_notif}' reçu de {envoyeur_notif}")

    else:
        print(f"Erreur dans la synchronization des fichiers : {response.status_code}")


def import_periodically(destinataire):
    while True:
        import_messages(destinataire)
        import_fichiers(destinataire)
        # Sleep for 5 seconds before running again
        time.sleep(5)


def display_messages(username, destinataire):
    messages_dir = f"MessagesDe_{username}/{destinataire}.json"

    # Check if the directory exists
    if not os.path.exists(messages_dir):
        print(f"Aucun message échangé avec {destinataire}")
        return

    # Ouvrir le fichier JSON et lire son contenu ligne par ligne
    with open(messages_dir, 'r') as file:
        lines = file.readlines()

    # Parcourir chaque ligne (chaque message) et l'afficher dans le format souhaité
    for line in lines:
        message = json.loads(line)
        envoyeur = message.get('envoyeur')
        timestamp = message.get('timestamp')
        message_text = message.get('message')

        print(f"From {envoyeur} at {timestamp}: {message_text}")

