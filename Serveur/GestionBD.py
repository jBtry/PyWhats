# Gère les accès aux bases de données

from pymongo import MongoClient
import sqlite3

# ----------------- MongoDB ---------------------

# Configuration de MongoDB client
mongo_client = MongoClient('mongodb://localhost:27017/') # en local sur le port par défaut
mongo_db = mongo_client['messagerie']  # Nom de la base de donnée messagerie
messages_collection = mongo_db['conversations']  # Contient les conversations
fichiers_collection = mongo_db['fichiers']


# ------------------ SQLite --------------------

# Se connecye à la table utilisateur
def get_sqlite_connection():
    conn = sqlite3.connect('utilisateurs.db')
    return conn


# Créer la table des utilisateurs, si elle n'existe pas deja ...
def create_users_table():
    conn = get_sqlite_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS utilisateurs 
                    (pseudo TEXT PRIMARY KEY NOT NULL,
                     mdp TEXT NOT NULL);''')
    conn.commit()
    conn.close()