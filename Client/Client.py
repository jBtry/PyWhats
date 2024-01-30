# Cette classe contient le MAIN du client

from Menu import *

# -------------------------------- MAIN --------------------------
while True:
    print(WELCOME + "\n")
    codeRetour, pseudo = menuAccueil();
    if codeRetour == 0 :
        pass
    elif codeRetour == 200: # Authentification validée par le serveur
        # TODO : threads de synchro
        menuFonctionnalites(pseudo)
    else : # codeRetour == 400
        pass






