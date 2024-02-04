# Contient toutes les requêtes susceptibles d'être envoyées par le client
# ainsi que des méthodes liées aux besoins métiers

import base64
import json
import os
import requests

from OutilsClient import *
from Textes import *

# Adresse du serveur
SERVER_URL = "http://127.0.0.1:61000"

# Crée un utilisateur
def creationCompte(pseudo, mdp):
    retour = requests.post(f"{SERVER_URL}/creationCompte", json={"pseudo": pseudo, "mdp": mdp})
    return retour.json(), retour.status_code

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


# Envoi de message
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

# Envoi de fichier
def envoyer_fichier(envoyeur, destinataire, filename, file_data, timestamp):
    
    file_data_base64 = base64.b64encode(file_data).decode('utf-8')

    response = requests.post(f"{SERVER_URL}/envoyer_fichier", json={"envoyeur": envoyeur, "destinataire": destinataire, "filename": filename, "file_data": file_data_base64, "timestamp": timestamp})
    
    pathname = f"FichiersDe_"+envoyeur+"/"+destinataire+".json"

    formatted_message = {
        "filename": filename,
        "file_data": file_data_base64,
        "destinataire": destinataire,
        "envoyeur": envoyeur,
        "timestamp": timestamp
    }    

    # Le répertoire existe ?
    if not os.path.exists("FichiersDe_"+envoyeur):
        # On crée le répertoire
        os.makedirs("FichiersDe_"+envoyeur)

    if not os.path.exists(pathname):
        with open(pathname, 'w') as file:
            file.write("")
    
    with open(pathname, 'a') as file:
        json.dump(formatted_message, file)
        file.write("\n")

 
    if response.status_code == 200:
        # Vérifie si la réponse contient des données JSON valides
        try:
            response_json = response.json()
            return response_json
        except json.JSONDecodeError as e:
            print(f"Erreur lors de la décodage de la réponse JSON : {e}")
            return {"error": "Erreur lors du décodage de la réponse JSON"}
    else:
        print(f"La requête a échoué avec le code d'état : {response.status_code}")
        return {"error": f"La requête a échoué avec le code d'état : {response.status_code}"}


# Synchro messages reçu
def synchro_messages(destinataire):

    if not os.path.exists("MessagesDe_"+destinataire):
        os.makedirs("MessagesDe_"+destinataire)
    
    response = requests.post(f"{SERVER_URL}/synchroniser_messages", json={"destinataire": destinataire})

    if response.status_code == 200:
        messages = json.loads(response.content.decode('utf-8'))  # Décode la réponse JSON

        if messages != []:
            cpt = 0
            envoyeur_notif = ""
            for message in messages:
                envoyeur = message.get('envoyeur')
                filename = f"MessagesDe_"+destinataire+"/"+envoyeur+".json"


                if not os.path.exists(filename):
                    with open(filename, 'w') as file:
                        file.write("")
                
                with open(filename, 'a') as file:
                    json.dump(message, file)
                    file.write("\n")
                
                envoyeur_notif = envoyeur
                cpt = cpt + 1

            print(f"\n                                              Tu as reçu {cpt} message(s) de {envoyeur_notif}")
                

    else:
        print(f"Erreur lors de la synchronisation des messages : {response.status_code}")


# Synchro fichiers reçu
def synchro_fichiers(destinataire):
    if not os.path.exists("FichiersDe_" + destinataire):
        os.makedirs("FichiersDe_" + destinataire)

    response = requests.post(f"{SERVER_URL}/synchroniser_fichiers", json={"destinataire": destinataire})

    if response.status_code == 200:
        files = json.loads(response.content.decode('utf-8'))

        if files != []:
            envoyeur_notif = ""
            filename_notif = ""

            for file_info in files:
                envoyeur = file_info.get('envoyeur')
                filename = file_info.get('filename')
                file_data_base64 = file_info.get('file_data')

                # Decode le fichier
                file_data = base64.b64decode(file_data_base64)

                # Sauvegarde le fichier
                file_path = f"FichiersDe_{destinataire}/{filename}"
                with open(file_path, 'wb') as file:
                    file.write(file_data)
                
                envoyeur_notif = envoyeur
                filename_notif = filename

            print(f"\n                                        Fichier '{filename_notif}' reçu de {envoyeur_notif}")

    else:
        print(f"Erreur dans la synchronization des fichiers : {response.status_code}")