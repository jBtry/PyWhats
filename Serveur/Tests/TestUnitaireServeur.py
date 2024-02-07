# Test des méthodes de OutilsServeur.py
# - Hachage du mot de passe "hashmdp"
# - Vérification du mot de passe "verifmdp"

from Serveur.OutilsServeur import *

mdp_original1 = "motdepasse123"
mdp_original2 = "motdepasse123."

# Test de la méthode hachage
print("-----Test de la méthode hachage-----")
mdp_hache1 = hashmdp(mdp_original1)
print(f"mdp_original1: {mdp_original1} => mdp_hache1: {mdp_hache1}")
mdp_hache2 = hashmdp(mdp_original2)
print(f"mdp_original2: {mdp_original2} => mdp_hache2: {mdp_hache2}")

# Test de la méthode de vérification
print("\n-----Test de la méthode de vérification du mot de passe -----")

print(f"Scénario 1 : Test de la méthode vérification avec le mot de passe 1 => {mdp_original1} et le hash associé => {mdp_hache1}")
print(f"La méthode doit retourner True")
verification_correcte = verifmdp(mdp_hache1, mdp_original1) # Retourne True
print(f"Le retour de la méthode est : {verification_correcte}\n")

print(f"Scénario 2 : Test de la méthode de vérification avec le mot de passe 2 => {mdp_original2} et le hash associé au mot de passe 1 => {mdp_hache1}")
print(f"La méthode doit retourner False")
verification_incorrecte = verifmdp(mdp_hache1, mdp_original2) # Retourne False
print(f"Le retour de la méthode est : {verification_incorrecte}\n")

if verification_correcte and not verification_incorrecte :
    print("Le test de la méthode de vérification du mot de passe a réussi")
else :
    print("Le test de la méthode de vérification du mot de passe a échoué")

