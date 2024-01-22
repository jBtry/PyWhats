import hashlib


def DemandeCreationCompte(client):
  # Demander le pseudo au client
  pseudo = input("Votre pseudo : ")

  # Vérifier que le pseudo est valide
  if not verificationPseudo(pseudo):
    return False

  # Demander le mot de passe au client
  mot_de_passe = input("Votre mot de passe : ")

  # Vérifier que le mot de passe est valide
  if not verificationMotDePasse(mot_de_passe):
    return False

  # Hasher le mot de passe
  mot_de_passe_hashe = hashlib.sha256(mot_de_passe.encode()).hexdigest()

  # Insérer le compte dans la base de données
  tuple_compte = (pseudo, mot_de_passe_hashe)
  insertion_ok = base_de_donnees.insert_tuple(tuple_compte)

  # Retourner le résultat de l'insertion
  return insertion_ok

def verificationPseudo(pseudo):
  """Vérifie si le pseudo est valide.

  Un pseudo valide doit contenir au moins 3 caractères et pas plus de 20 caractères.

  Args:
    pseudo: Le pseudo à vérifier.

  Returns:
    True si le pseudo est valide, False sinon.
  """

  if len(pseudo) < 3 or len(pseudo) > 20:
    return False

  return True

def verificationMotDePasse(mot_de_passe):
  """Vérifie si le mot de passe est valide.

  Un mot de passe valide doit contenir au moins 8 caractères et au moins une lettre majuscule, une lettre minuscule, un chiffre et un caractère spécial.

  Args:
    mot_de_passe: Le mot de passe à vérifier.

  Returns:
    True si le mot de passe est valide, False sinon.
  """

  if len(mot_de_passe) < 8:
    return False

  caracteres_valides = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+")
  for caractere in mot_de_passe:
    if caractere not in caracteres_valides:
      return False

  return True