# Contient les différents menus de l'application

from Textes import *
from Requetes import *
from OutilsClient import *

def demanderChoix() :
    return input(CHOIX)

def menuAccueil() :
    while True :
        print(MENU_ACCUEIL)
        choix = demanderChoix()
        if choix == '1': # Créer un compte
            pseudoOK = False
            mdpOK = False
            while not pseudoOK :
                pseudo = input("Saisir le pseudo : ")
                if verificationPseudo(pseudo) :
                    pseudoOK = True
                else :
                    print(MESSAGE_PSEUDO_INVALIDE)
            while not mdpOK:
                mdp = input("Saisir le mot de passe : ")
                if verificationMDP(mdp) :
                    mdpOK = True
                else :
                    print(MESSAGE_MDP_INVALIDE)
            print(creationCompte(pseudo, mdp))
            return 0, ""

        elif choix == '2': # Se connecter
            pseudo = input("Saisir le pseudo : ")
            mdp = input("Saisir le mot de passe : ")
            codeErreur = seConnecter(pseudo, mdp)
            return codeErreur, pseudo

        elif choix == '3': # Quitter
            print(MESSAGE_QUITTER)
            exit(0)

        else :
            print(MESSAGE_ERREUR_MENU_TROIS_CHOIX)


def menuFonctionnalites(pseudo) :
    while True :
        print(FCT + "\n")
        choix = demanderChoix()
        if choix == '1': # Envoyer un message
            destinataire = input("Saisir le pseudo du destinataire: ")
            while True:
                if verificationUtilisateur(destinataire):
                    menuEnvoiMessage(destinataire)
                    choix = demanderChoix()
                    if choix == '1':
                        afficherMessages(pseudo, destinataire)
                        message = input("Saisir un message (x pour retour): ")
                        if message == 'x':
                            break
                        print(envoyer_message(pseudo, destinataire, message, return_timestamp()))
                    elif choix == '2':
                        break
                    else:
                        print(MESSAGE_ERREUR_MENU_DEUX_CHOIX)
                else:
                    print("Ce destinataire n'existe pas")
                    break

        elif choix == '2': # Envoyer un fichier
            destinataire = input("Saisir le pseudo du destinataire: ")
            while True:
                if verificationUtilisateur(destinataire):
                    menuEnvoiFichier(destinataire)
                    choix = demanderChoix()
                    if choix == '1':
                        chemin_fichier = input("Saisir le chemin du fichier : ")

                        if os.path.exists(chemin_fichier):
                            with open(chemin_fichier, 'rb') as fichier:
                                donnees_fichier = fichier.read()

                            nom_fichier = os.path.basename(chemin_fichier)
                            print(envoyer_fichier(pseudo, destinataire, nom_fichier, donnees_fichier, return_timestamp()))
                            time.sleep(5)
                        
                        else:
                            print("Fichier non trouvé. Saisir un chemin du fichier valide.")

                    elif choix == '2':
                        break
                    else:
                        print(MESSAGE_ERREUR_MENU_DEUX_CHOIX)
                else:
                    print("Ce destinataire n'existe pas")
                    break

        elif choix == '3': # Gérer son profil
            while True:
                menuGererProfil()
                choix = demanderChoix()
                pseudoOK = False
                mdpOK = False
                if choix =='1': # Changer pseudo
                    while not pseudoOK:
                        nouveau_pseudo = input("Saisir le pseudo : ")
                        if verificationPseudo(pseudo):
                            pseudoOK = True
                            reponse = changer_pseudo(pseudo, nouveau_pseudo)
                            print(reponse)
                        else:
                            print(MESSAGE_PSEUDO_INVALIDE)
                
                elif choix =='2': # Changer mdp
                    while not mdpOK:
                        nouveau_mdp = input("Saisir le mot de passe : ")
                        if verificationMDP(nouveau_mdp):
                            mdpOK = True
                            reponse = changer_mdp(pseudo, nouveau_mdp)
                            print(reponse)
                        else:
                            print(MESSAGE_MDP_INVALIDE)

                elif choix =='3':
                    break

                else:
                    print(MESSAGE_ERREUR_MENU_TROIS_CHOIX)

        elif choix == '4': # Supprimer une conversation
            destinataire = input("Saisir le pseudo du destinataire: ")
            while True:
                if verificationUtilisateur(destinataire): # pseudo Valide
                    afficherMessages(pseudo, destinataire)
                    menuSupprimerConversation(destinataire)
                    choix = demanderChoix()

                    if choix == '1':
                        print(suppConversation(pseudo, destinataire))

                    elif choix == '2':
                        break
                    else:
                        print(MESSAGE_ERREUR_MENU_DEUX_CHOIX)
                else:
                    print("Ce destinataire n'existe pas")
                    break

        elif choix == '5': # Se déconnecter
            break

        else:
            print(MESSAGE_ERREUR_MENU_CINQ_CHOIX)


def menuEnvoiMessage(destinataire):
    print(MENU_ENVOI_MESSAGE % destinataire)

def menuEnvoiFichier(destinataire):
    print(MENU_ENVOI_FICHIER % destinataire)

def menuSupprimerConversation(destinataire):
    print(MENU_SUPPRIMER % destinataire)

def menuGererProfil():
    print(MENU_GERER_PROFIL)