# Met à disposition, pour le client, différents outils
# - Récupérer le timestamp
# - Vérifier que le pseudo est conforme
# - Vérifier que le mot de passe est conforme
# - Supprimer une conversation

import os, re, tzlocal
from datetime import datetime

def get_horodatage():
    timezone = tzlocal.get_localzone()
    horodatage = datetime.now(timezone)
    formatted_timestamp = horodatage.strftime("%H:%M %d/%m/%Y")
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

    return bool(re.fullmatch(pattern, mdp))

# Fonction pour supprimer une conversation
def suppConversation(pseudo, destinataire):
    # Chemin du fichier JSON de la conversation
    filepath = f"MessagesDe_{pseudo}/{destinataire}.json"

    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"La conversation avec {destinataire} a été supprimé.")
    else:
        print(f"Aucune conversation trouvée avec {destinataire}.")
