# Test des méthodes de OutilsClient.py
from Client.OutilsClient import *
def TEST_verificationMDP():
    # Test de la fonction avec différents mots de passe
    test_passwords = [
        "Password123!",       # Doit retourner True
        "password123!",       # Doit retourner False (pas de majuscule)
        "Password!",          # Doit retourner False (pas de chiffre)
        "Password123",        # Doit retourner False (pas de caractère spécial)
        "Pw1!",               # Doit retourner False (moins de 12 caractères)
        "P"*81 + "assword123!", # Doit retourner False (plus de 80 caractères)
        "Password123!$",      # Doit retourner True
        "Aa1!" + "a"*8,       # Doit retourner True (juste 12 caractères)
        "ValidPassword123$!"  # Doit retourner True
    ]

    # Application de la fonction sur chaque mot de passe
    for mdp in test_passwords :
        resultat = verificationMDP(mdp)
        print(f"'{mdp}': {resultat}")

def TEST_verificationPseudo():
    pass
def TEST_suppConversation():
    pass
def TEST_timestamp():
    pass

# --------------- MAIN -------------
# Lancement des Tests...



