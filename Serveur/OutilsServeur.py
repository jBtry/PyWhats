# Met à disposition, pour le serveur, différents outils
# - Hachage du mot de passe
# - Vérification du mot de passe

import bcrypt

# Permet le hachage du mot de passe
def hashmdp(mdp):
    return bcrypt.hashpw(mdp.encode('utf-8'), bcrypt.gensalt())


# Vérifie le mot de passe
def verifmdp(mdpEnBD, mdpSaisi):
    return bcrypt.checkpw(mdpSaisi.encode('utf-8'), mdpEnBD)
