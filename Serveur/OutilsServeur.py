# Met à disposition, pour le serveur, différents outils
# - Hachage du mot de passe
# - Vérification du mot de passe

import bcrypt

# Permet le hachage du mot de passe
def hashmdp(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


# Vérifie le mot de passe
def verifmdp(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)
