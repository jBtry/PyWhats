def authentifier(client):
  """S'authentifie sur le serveur.

  Args:
    client: Le client qui s'authentifie.

  Returns:
    True si l'authentification a réussi, False sinon.
  """

  # Demander le pseudo au client
  pseudo = input("Votre pseudo : ")

  # Vérifier que le pseudo est valide
  if not pseudoUnique(pseudo):
    return False

  # Vérifier que le pseudo existe dans la base de données
  tuple_compte = (pseudo, None)
  compte_existe = base_de_donnees.select_tuple(tuple_compte)
  if not compte_existe:
    return False

  # Demander le mot de passe au client
  mot_de_passe = input("Votre mot de passe : ")

  # Vérifier que le mot de passe correspond au mot de passe enregistré dans la base de données
  hash_mot_de_passe_enregistre = compte_existe[1]
  if hashlib.sha256(mot_de_passe.encode()).hexdigest() != hash_mot_de_passe_enregistre:
    return False

  # L'authentification a réussi
  return True


# A modifer
def pseudoUnique(pseudo):
  """Vérifie si le pseudo est unique.

  Un pseudo valide doit contenir au moins 3 caractères et pas plus de 20 caractères.

  Args:
    pseudo: Le pseudo à vérifier.

  Returns:
    True si le pseudo est valide, False sinon.
  """

  if len(pseudo) < 3 or len(pseudo) > 20:
    return False

  return True
