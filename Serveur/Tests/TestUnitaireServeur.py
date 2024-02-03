# Test des méthodes de OutilsServeur.py
# - Hachage du mot de passe "hashmdp"
# - Vérification du mot de passe "verifmdp"

from Serveur.OutilsServeur import *

mdp_original1 = "motdepasse123"
mdp_original2 = "motdepasse123."
compteurTestOk = 0

# Test de la méthode hachage
print("-----Test de la méthode hachage-----")
mdp_hache1 = hashmdp(mdp_original1)
print(f"mdp_original1: {mdp_original1} => mdp_hache1: {mdp_hache1}")
mdp_hache2 = hashmdp(mdp_original2)
print(f"mdp_original2: {mdp_original2} => mdp_hache2: {mdp_hache2}")

# Test de la méthode de vérification
print("-----Test de la méthode de vérification du mot de passe -----")
verification_correcte = verifmdp(mdp_hache1, mdp_original1) # Retourne True
verification_incorrecte = verifmdp(mdp_hache1, mdp_original2) # Retourne False
if verification_correcte and not verification_incorrecte :
    print("Le test de la méthode de vérification du mot de passe a réussi")
else :
    print("Le test de la méthode de vérification du mot de passe a échoué")

