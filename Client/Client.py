# Ce fichier contient le MAIN du client

import threading
from Menu import *

# -------------------------------- MAIN --------------------------
while True:
    print(WELCOME + "\n")
    codeRetour, pseudo = menuAccueil();
    if codeRetour == 0 :
        pass
    elif codeRetour == 200: # Authentification validée par le serveur
        import_messages_thread = threading.Thread(target=importPeriodique, args=(pseudo,))
        import_messages_thread.daemon = True
        import_messages_thread.start()
        menuFonctionnalites(pseudo)
    else : # codeRetour == 400
        pass






