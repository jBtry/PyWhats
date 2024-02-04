# Test les méthodes de OutilsClient.py
from Client.OutilsClient import *
def TEST_verificationMDP():
    print("---------------- TEST verificationMDP() ------------------")
    # Test de la fonction avec différents mots de passe
    test = [
        ("Password123!", True),         # Doit retourner True
        ("password123!", False),         # Doit retourner False (pas de majuscule)
        ("Password!", False),            # Doit retourner False (pas de chiffre)
        ("Password123", False),          # Doit retourner False (pas de caractère spécial)
        ("Pw1!", False),                 # Doit retourner False (moins de 12 caractères)
        ("P"*81 + "assword123!", False), # Doit retourner False (plus de 80 caractères)
        ("Password123!$", True),         # Doit retourner True
        ("Aa1!" + "a"*8, True),          # Doit retourner True (juste 12 caractères)
        ("ValidPassword123$!", True),    # Doit retourner True
    ]

    cptReussite = 0
    # Application de la fonction sur chaque mot de passe et affichage du résultat
    for mdp, attendu in test:
        resultat = verificationMDP(mdp)
        resultat_test = 'réussi' if resultat == attendu else 'échoué'
        if resultat_test == 'réussi' :
            cptReussite += 1
        print(f"Test avec '{mdp}': attendu = {attendu}, obtenu = {resultat} - {resultat_test}")

    if cptReussite == len(test):
        print("Tous les tests ont réussi")
    else:
        print("Au moins un test a échoué")



def TEST_verificationPseudo():
    print("\n---------------- TEST verificationPSEUDO() ------------------")
    # Test de la fonction avec plusieurs pseudos
    test = [
        ("Valide", True),
        ("123", True),
        ("123456789012345", True),
        ("Ve", False),
        ("", False),
        ("1234567890123456", False),
        ("abcdefghijklmnop", False)
    ]

    cptReussite = 0
    for i, (pseudo, attendu) in enumerate(test, 1):
        result = verificationPseudo(pseudo)
        if result == attendu:
            print(f"Test {i} avec pseudo '{pseudo}': SUCCÈS")
            cptReussite += 1
        else:
            print(f"Test {i} avec pseudo '{pseudo}': ÉCHEC (attendu: {attendu}, obtenu: {result})")

    if cptReussite == len(test):
        print("Tous les tests ont réussi")
    else :
        print("Au moins un test a échoué")

def TEST_suppConversation():
    print("\n---------------- TEST suppConversation() ------------------")
    pseudo = "utilisateurTest"
    destinataire_existant = "ami"
    destinataire_inexistant = "inconnu"

    # Préparation
    os.makedirs(f"MessagesDe_{pseudo}")
    with open(f"MessagesDe_{pseudo}/{destinataire_existant}.json", "w") as f:
        f.write("Contenu test")

    print("Test 1: Suppression d'une conversation existante")
    suppConversation(pseudo, destinataire_existant)
    if os.path.exists(f"MessagesDe_{pseudo}/{destinataire_existant}.json") :
        print("ECHEC DU TEST => Le fichier aurait dû être supprimé")
    else :
        print("REUSSITE DU TEST => Le fichier été supprimé")

    print("Test 2: Tentative de suppression d'une conversation inexistante")
    print(f"La fonction doit afficher : Aucune conversation trouvée avec {destinataire_inexistant}.")
    print("------------- RESULTAT FONCTION -------------\n")
    suppConversation(pseudo, destinataire_inexistant)
    print("---------------------------------------------\n")

    # Nettoyage après le test
    if os.path.isdir(f"MessagesDe_{pseudo}"):
        for fichier in os.listdir(f"MessagesDe_{pseudo}"):
            os.remove(f"MessagesDe_{pseudo}/{fichier}")
        os.rmdir(f"MessagesDe_{pseudo}")



def TEST_get_horodatage():
    print("\n---------------- TEST get_horodatage() ------------------")
    print("Vérification du format attendu")
    horodatage = get_horodatage()
    print(horodatage)
    resultat = bool(re.fullmatch(r"\d{2}:\d{2} \d{2}/\d{2}/\d{4}", horodatage))
    if resultat :
        print("REUSSITE DU TEST => Le timestamp correspond au format attendu.")
    else :
        print("ECHEC DU TEST => Le timestamp ne correspond pas au format attendu.")

    print("On génère un timestamp, pour valider le test, celui-ci doit être à la date du jour\n"
          "et proche de l'heure actuelle (une minute d'intervalle maximum)")
    print("-------------------- TIMESTAMP ACTUEL -----------------------------")
    print(get_horodatage())
    print("-------------------------------------------------------------------")


def TEST_afficherConversation():
    print("\n---------------- TEST afficherConversation() ------------------")

    # Création des élements nécessaire pour le test
    messages = [
        {"envoyeur": "Leo", "timestamp": "2023-01-01 12:00", "message": "Salut !"},
        {"envoyeur": "Guillaume", "timestamp": "2023-01-01 12:01", "message": "Hey !, comment ça va ?"}
    ]
    pseudo = "Leo"
    destinataire = "Guillaume"
    os.makedirs(f"MessagesDe_{pseudo}")
    with open(f"MessagesDe_{pseudo}/{destinataire}.json", 'w') as f:
        for message in messages:
            f.write(json.dumps(message) + '\n')


    print("Vérification de l'affichage correcte d'une conversation\n")

    # Scénario 1: Messages existants
    print("Scénario 1: Messages existants\n")
    afficherConversation('Leo', 'Guillaume')

    # Scénario 2: Aucun message échangé (Pas besoin de créer de fichier pour ce test)
    print("\nScénario 2: Aucun message échangé")
    afficherConversation('Leo', 'Clement')

    # Nettoyage
    if os.path.isdir(f"MessagesDe_{pseudo}"):
        for fichier in os.listdir(f"MessagesDe_{pseudo}"):
            os.remove(f"MessagesDe_{pseudo}/{fichier}")
        os.rmdir(f"MessagesDe_{pseudo}")


# --------------- MAIN -------------
# Lancement des Tests...
TEST_verificationMDP()
TEST_verificationPseudo()
TEST_suppConversation()
TEST_get_horodatage()
TEST_afficherConversation()


