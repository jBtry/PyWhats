# Contient toutes les requêtes susceptibles d'être envoyées par le client
# ainsi que des méthodes liées aux besoins métiers

import base64, json, os, requests, time
from threading import Lock
from OutilsClient import verificationMDP
from Textes import *

# Dictionnaire pour stocker les verrous par nom de fichier
verrous = {}

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
    reponse = requests.post(f"{SERVER_URL}/envoyer_message", json={"envoyeur": envoyeur, "destinataire": destinataire, "message": message, "timestamp": timestamp})
    nomfichier = f"MessagesDe_"+envoyeur+"/"+destinataire+".json"
    message_format = '{"message": "' + message + '", "destinataire": "' + destinataire + '", "envoyeur": "' + envoyeur + '", "timestamp": "' + timestamp + '"}'

    if not os.path.exists("MessagesDe_"+envoyeur):
        os.makedirs("MessagesDe_"+envoyeur)

    verrou = obtenir_verrou(nomfichier)
    with verrou :
        if not os.path.exists(nomfichier):
            with open(nomfichier, 'w') as file:
                file.write("")

        with open(nomfichier, 'a') as file:
            file.write(message_format)
            file.write("\n")

    return reponse.json()

# Envoi de fichier
def envoyer_fichier(envoyeur, destinataire, filename, file_data, timestamp):
    
    file_data_base64 = base64.b64encode(file_data).decode('utf-8')
    reponse = requests.post(f"{SERVER_URL}/envoyer_fichier", json={"envoyeur": envoyeur, "destinataire": destinataire, "filename": filename, "file_data": file_data_base64, "timestamp": timestamp})
    nomfichier = f"MessagesDe_"+envoyeur+"/"+destinataire+".json"
    message = f"Le fichier : {filename} a été envoyé"
    message_format = '{"message": "' + message + '", "destinataire": "' + destinataire + '", "envoyeur": "' + envoyeur + '", "timestamp": "' + timestamp + '"}'

 
    if reponse.status_code == 200:
        # Vérifie si la réponse contient des données JSON valides
        try:
            reponse_json = reponse.json()
            if not os.path.exists("FichiersDe_" + envoyeur):
                os.makedirs("FichiersDe_" + envoyeur)

            verrou = obtenir_verrou(nomfichier)
            with verrou:
                if not os.path.exists(nomfichier):
                    with open(nomfichier, 'w') as file:
                        file.write("")

                with open(nomfichier, 'a') as file:
                    file.write(message_format)
                    file.write("\n")
            return reponse_json
        except json.JSONDecodeError as e:
            print(f"Erreur lors de la décodage de la réponse JSON : {e}")
            return {"error": "Erreur lors du décodage de la réponse JSON"}
    else:
        print(f"La requête a échoué avec le code d'état : {reponse.status_code}")
        return {"error": f"La requête a échoué avec le code d'état : {reponse.status_code}"}


# Synchro messages reçu
def synchro_messages(destinataire):

    if not os.path.exists("MessagesDe_"+destinataire):
        os.makedirs("MessagesDe_"+destinataire)
    
    reponse = requests.post(f"{SERVER_URL}/synchroniser_messages", json={"destinataire": destinataire})

    if reponse.status_code == 200:
        messages = json.loads(reponse.content.decode('utf-8'))  # Décode la réponse JSON

        if messages != []:
            cpt = 0
            envoyeur_notif = ""
            for message in messages:
                envoyeur = message.get('envoyeur')
                nomfichier = f"MessagesDe_"+destinataire+"/"+envoyeur+".json"

                verrou = obtenir_verrou(nomfichier)
                with verrou:
                    if not os.path.exists(nomfichier):
                        with open(nomfichier, 'w') as file:
                            file.write("")

                    with open(nomfichier, 'a') as file:
                        json.dump(message, file)
                        file.write("\n")
                
                envoyeur_notif = envoyeur
                cpt = cpt + 1

            print(f"\n                                              Tu as reçu {cpt} message(s) de {envoyeur_notif}")
                

    else:
        print(f"Erreur lors de la synchronisation des messages : {reponse.status_code}")


# Synchro fichiers reçu
def synchro_fichiers(destinataire):
    if not os.path.exists("FichiersDe_" + destinataire):
        os.makedirs("FichiersDe_" + destinataire)

    reponse = requests.post(f"{SERVER_URL}/synchroniser_fichiers", json={"destinataire": destinataire})

    if reponse.status_code == 200:
        files = json.loads(reponse.content.decode('utf-8'))

        if files != []:
            envoyeur_notif = ""
            filename_notif = ""

            for file_info in files:
                envoyeur = file_info.get('envoyeur')
                nomfichier = file_info.get('nomfichier')
                file_data_base64 = file_info.get('donnees')
                timestamp = file_info.get('timestamp')

                # Decode le fichier
                file_data = base64.b64decode(file_data_base64)

                # Sauvegarde le fichier
                file_path = f"FichiersDe_{destinataire}/{nomfichier}"
                with open(file_path, 'wb') as file:
                    file.write(file_data)
                
                envoyeur_notif = envoyeur
                filename_notif = nomfichier

            print(f"\n                                        Fichier '{filename_notif}' reçu de {envoyeur_notif}")

            nomConversation = f"MessagesDe_"+destinataire+"/"+envoyeur+".json"
            message = f"Le fichier : {nomfichier} a été reçu"
            message_format = '{"message": "' + message + '", "destinataire": "' + destinataire + '", "envoyeur": "' + envoyeur + '", "timestamp": "' + timestamp + '"}'
            verrou = obtenir_verrou(nomConversation)
            with verrou:
                if not os.path.exists(nomfichier):
                    with open(nomfichier, 'w') as file:
                        file.write("")

                with open(nomfichier, 'a') as file:
                    file.write(message_format)
                    file.write("\n")

    else:
        print(f"Erreur dans la synchronization des fichiers : {reponse.status_code}")

# Vérifier si l'utilisateur a reçu des messages et des fichiers
def importPeriodique(destinataire):
    while True:
        synchro_messages(destinataire)
        synchro_fichiers(destinataire)
        time.sleep(5)

# Génère un verrou pour les accès concurrent au fichier JSON
# contenant les conversations
def obtenir_verrou(nom_fichier):
    if nom_fichier not in verrous:
        verrous[nom_fichier] = Lock()
    return verrous[nom_fichier]