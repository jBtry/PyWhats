# Instancie le service web servant à écouter les requêtes des clients,
# ce fichier contient les endpoints et le traitement associé à chacun d'eux

import base64
from OutilsServeur import *
from GestionBD import *
from flask import Flask, request, jsonify

# Crée une instance de la classe Flask
# app est la variable contenant cette instance, c'est l'application web elle-même.
# Celle-ci gère les requêtes et les réponses
app = Flask(__name__)

# Le décorateur "@app.route" représente l'URL du serveur.
# Cela évite d'écrire dans notre cas, http://ip_serveur:61000/endpoints
# la liste "methods" précise les méthodes HTTP autorisé sur ce endpoint,
# dans le cas de l'endpoint ci-dessus seul la méthode POST est autorisée

# Cet endpoint permet de créer un compte utilisateur
@app.route('/creationCompte', methods=['POST'])
def creerCompte():
    # Extraction du pseudo and du mot de passe de la requête (matérialisé par un JSON)
    pseudo = request.json['pseudo']
    mdp = request.json['mdp']

    # Hachage du mot de passe
    hashed_mdp = hashmdp(mdp)

    # Insère le couple pseudo/mot de passe dans la base de donnée
    conn = get_sqlite_connexion()
    try:
        conn.execute('INSERT INTO utilisateurs (pseudo, mdp) VALUES (?, ?)',
                     (pseudo, hashed_mdp))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        return jsonify("Le pseudo existe déjà !"), 400
    finally:
        conn.close()

    return jsonify("L\'utilisateur a bien été enregistré"), 201

# Vérifie le pseudo
@app.route('/verificationUtilisateur', methods=['POST'])
def verificationUtilisateur():

    pseudo = request.json['pseudo']

    if not pseudo:
        return jsonify("Erreur, le pseudo est requis"), 400

    conn = sqlite3.connect('utilisateurs.db')
    cursor = conn.cursor()

    # Vérifie l'existence du nom d'utilisateur
    cursor.execute('SELECT * FROM utilisateurs WHERE pseudo = ?', (pseudo,))
    user = cursor.fetchone()

    conn.close()

    # Envoi le résultat en fonction de si l'utilisateur a été trouvé ou non
    if user:
        return jsonify(True), 200
    else:
        return jsonify(False), 200


# Connexion
@app.route('/seConnecter', methods=['POST'])
def seConnecter():

    pseudo = request.json['pseudo']
    mdp = request.json['mdp']

    conn = get_sqlite_connexion()
    cursor = conn.execute('SELECT mdp FROM utilisateurs WHERE pseudo=?', (pseudo,))
    user = cursor.fetchone()
    conn.close()

    # Verifying mdp
    if user and verifmdp(user[0], mdp):
        return jsonify("Connexion réussi"), 200
    else:
        return jsonify("Pseudo ou Mot de passe invalide"), 403

# Change le pseudo
@app.route('/changer_pseudo', methods=['POST'])
def changer_pseudo():

    pseudo_actuel = request.json['pseudo_actuel']
    new_pseudo = request.json['new_pseudo']

    if not pseudo_actuel:
        return jsonify({'error': 'pseudo is required'}), 400

    conn = sqlite3.connect('utilisateurs.db')
    cursor = conn.cursor()

    # Vérifie l'existence du nom d'utilisateur
    cursor.execute('SELECT * FROM utilisateurs WHERE pseudo = ?', (pseudo_actuel,))
    user = cursor.fetchone()

    conn.close()
    if user:
        conn = get_sqlite_connexion()
        try:
            conn.execute('UPDATE utilisateurs SET pseudo =? WHERE pseudo =?',
                         (new_pseudo, pseudo_actuel))
            conn.commit()
        except sqlite3.IntegrityError:
            return jsonify("Erreur dans la mise à jour du pseudo"), 500
        finally:
            conn.rollback()
            conn.close()

        return jsonify("Pseudo changé avec succès !"), 201
        
    else:
        return jsonify("Le pseudo existe déjà"), 400


# Change le mot de passe
@app.route('/changer_mdp', methods=['POST'])
def changer_mdp():
    pseudo = request.json['pseudo']
    new_mdp = request.json['new_mdp']

    hashed_mdp = hashmdp(new_mdp)

    conn = get_sqlite_connexion()
    try:
        conn.execute('UPDATE utilisateurs SET mdp =? WHERE pseudo =?',
                     (hashed_mdp, pseudo))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        return jsonify("Erreur lors de la mise à jour du mot de passe, aucune modification n\'a été effectué"), 500
    finally:
        conn.close()

    return jsonify("Le mot de passe a bien été changé !"), 201


# Envoi message
@app.route('/envoyer_message', methods=['POST'])
def envoyer_message():
    # Extraction des infos de la requête
    envoyeur = request.json['envoyeur']
    destinataire = request.json['destinataire']
    message_text = request.json['message']
    timestamp = request.json['timestamp']

    message = {
        'envoyeur': envoyeur,
        'destinataire': destinataire,
        'message': message_text,
        'timestamp': timestamp
    }

    # Enregistrement dans mongoDB
    result = messages_collection.insert_one(message)

    if result.acknowledged:
        return jsonify("Message envoyé avec succès"), 200
    else:
        return jsonify("Erreur: le message n\'a pas été envoyé"), 500


# Envoi de fichier
@app.route('/envoyer_fichier', methods=['POST'])
def envoyer_fichier():
    # Extraction des informations contenue dans la requête
    envoyeur = request.json['envoyeur']
    destinataire = request.json['destinataire']
    file_data_base64 = request.json['file_data']
    filename = request.json['filename']
    timestamp = request.json['timestamp']

    file_data = base64.b64decode(file_data_base64)

    file = {
    'envoyeur': envoyeur,
    'destinataire': destinataire,
    'filename': filename,
    'file_data': file_data,
    'timestamp': timestamp
    }

    # Insertion dans la BD
    result = fichiers_collection.insert_one(file)

    if result.acknowledged:
        return jsonify("Fichier envoyé avec succès"), 200
    else:
        return jsonify("Erreur: le fichier n\'a pas été envoyé"), 500


# Distribue les messages
@app.route('/synchroniser_messages', methods=['POST'])
def synchroniser_messages():

    destinataire = request.json['destinataire']
    messages = messages_collection.find({'destinataire': destinataire})
    synchronized_messages = []

    # Ajouter chaque message à la liste synchronisée
    for message in messages:
        synchronized_messages.append({
            'envoyeur': message['envoyeur'],
            'destinataire': message['destinataire'],
            'message': message['message'],
            'timestamp': message['timestamp']
        })

    criteria = {'destinataire': destinataire}
    deleted_result = messages_collection.delete_many(criteria)
    print(f"Number of messages deleted: {deleted_result.deleted_count}")

    return jsonify(synchronized_messages), 200


@app.route('/synchroniser_fichiers', methods=['POST'])
def synchroniser_fichiers():

    destinataire = request.json['destinataire']

    files = fichiers_collection.find({'destinataire': destinataire})

    synchronized_files = []

    # Ajouter chaque message à la liste synchronisée
    for file in files:
        envoyeur = file['envoyeur']
        destinataire = file['destinataire']
        filename = file['filename']
        file_data = file['file_data']
        timestamp = file['timestamp']
    
        file_data_base64 = base64.b64encode(file_data).decode('utf-8')

        synchronized_files.append({
            'envoyeur': envoyeur,
            'destinataire': destinataire,
            'filename': filename,
            'file_data': file_data_base64,
            'timestamp': timestamp
        })
    
    critere = {'destinataire': destinataire}
    deleted_result = fichiers_collection.delete_many(critere)
    print(f"Number of files deleted: {deleted_result.deleted_count}")

    return jsonify(synchronized_files), 200