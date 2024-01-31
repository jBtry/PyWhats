# Met à disposition, pour le serveur, différents outils
# - Récupérer le timestamp

import os
import re
from datetime import datetime
import pytz

def return_timestamp():
    # Get the current time in UTC
    utc_now = datetime.now(pytz.utc)

    # Format the timestamp as required
    formatted_timestamp = utc_now.strftime("%H:%M %d/%m/%Y")

    return formatted_timestamp

# Vérifie que le pseudo respecte les specs fonctionnelles
def verificationPseudo(pseudo) :
    return 3 <= len(pseudo) <= 15

# Vérifie que le mot de passe respecte les specs fonctionnelles
def verificationMDP(mdp) :
    # REGEX
    pattern = r'^(?=.*[!@#$%^&*()_+{}[\]:;<>,.?~])'  # Au moins un caractère spécial
    pattern += r'(?=.*[a-z])'  # Au moins une minuscule
    pattern += r'(?=.*[A-Z])'  # Au moins une majuscule
    pattern += r'(?=.*\d)'  # Au moins un nombre
    pattern += r'.{12,80}$'  # Entre 12 et 80 caractères inclus

    return re.match(pattern, mdp)

# Fonction pour supprimer une conversation
def delete_conversation(username, receiver):
    # Chemin du fichier JSON de la conversation
    filepath = f"MessagesDe_{username}/{receiver}.json"

    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Conversation with {receiver} has been deleted.")
    else:
        print(f"No conversation found with {receiver}.")
