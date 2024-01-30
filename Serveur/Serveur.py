# MAIN du serveur

from GestionBD import *
from Traitement import *

# --------- MAIN -------
# On crée la table des utilisateurs au démarrage, si elle n'existe pas deja ... cf. GestionBD.create_users_table
# On démarre le serveur web, celui-ci écoute sur toutes les interfaces de la machine
# Le port d'écoute est le 61000
# Le mode debug permet de recharger automatiquement l'application quand le code source est modifié.
if __name__ == '__main__':
    create_users_table()
    app.run(host='0.0.0.0', port=61000, debug=True)


