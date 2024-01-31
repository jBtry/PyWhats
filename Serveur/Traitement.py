# Instancie le service web servant à écouter les requêtes des clients,
# elle contient les endpoints et le traitement associé à chacun d'eux

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
def register():
    # Extraction du pseudo and du mot de passe de la requête (matérialisé par un JSON)
    pseudo = request.json['pseudo']
    mdp = request.json['mdp']

    # Hachage du mot de passe
    hashed_mdp = hashmdp(mdp)

    # Insère le couple pseudo/mot de passe dans la base de donnée
    conn = get_sqlite_connection()
    try:
        conn.execute('INSERT INTO utilisateurs (pseudo, mdp) VALUES (?, ?)',
                     (pseudo, hashed_mdp))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        return jsonify({'message': 'Le pseudo existe deja'}), 400
    finally:
        conn.close()

    return jsonify({'message': 'L\'utilisateur a bien été enregistré'}), 201

# Vérifie le pseudo
@app.route('/verificationUtilisateur', methods=['POST'])
def verificationUtilisateur():

    pseudo = request.json['pseudo']

    if not pseudo:
        return jsonify({'error': 'Username is required'}), 400

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
def login():

    pseudo = request.json['pseudo']
    mdp = request.json['mdp']

    conn = get_sqlite_connection()
    cursor = conn.execute('SELECT mdp FROM utilisateurs WHERE pseudo=?', (pseudo,))
    user = cursor.fetchone()
    conn.close()

    # Verifying mdp
    if user and verifmdp(user[0], mdp):
        return jsonify({'message': 'Connexion réussi'}), 200
    else:
        return jsonify({'message': 'Pseudo ou Mot de passe invalide'}), 403

# Change le pseudo
@app.route('/changer_pseudo', methods=['POST'])
def changer_pseudo():

    pseudo_actuel = request.json['current-username']
    new_pseudo = request.json['new_username']

    already_exist = verificationUtilisateur(new_pseudo)

    if already_exist:
        return jsonify({'message': 'le pseudo existe deja'}), 400
    else:
        conn = get_sqlite_connection()
        try:
            conn.execute('UPDATE users SET username =? WHERE username =?',
                         (new_pseudo, pseudo_actuel))
            conn.commit()
        except sqlite3.IntegrityError:
            return jsonify({'message': 'Error updating the username'}), 400 # TODO : changer code erreur
        finally:
            conn.rollback()
            conn.close()

        return jsonify({'message': 'Username changed successfully'}), 201

# Change le mot de passe
@app.route('/changer_mdp', methods=['POST'])
def changer_mdp():
    pseudo = request.json['pseudo']
    new_mdp = request.json['new_mdp']

    hashed_password = hashmdp(new_mdp)

    conn = get_sqlite_connection()
    try:
        conn.execute('UPDATE users SET password =? WHERE pseudo =?',
                     (hashed_password, pseudo))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        return jsonify({'message': 'Erreur lors de la mise à jour du mot de passe, aucune modification n\'a été effectué'}), 400
    finally:
        conn.close()

    return jsonify({'message': 'Le mot de passe a été changé !'}), 201


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

    # Adding message to an existing conversation in MongoDB
    messages_collection.insert_one(message)

    return jsonify({'message': 'Message sent successfully'}), 200


# Flask route for sending a message
@app.route('/send_file', methods=['POST'])
def send_file():
    # Extracting sender and message from request
    sender = request.json['sender']
    receiver = request.json['receiver']
    file_data_base64 = request.json['file_data']
    filename = request.json['filename']
    timestamp = request.json['timestamp']

    file_data = base64.b64decode(file_data_base64)

    file = {
    'sender': sender,
    'receiver': receiver,
    'filename': filename,
    'file_data': file_data,
    'timestamp': timestamp
    }

    # Adding message to an existing conversation in MongoDB
    result = fichiers_collection.insert_one(file)

    if result.acknowledged:
        return jsonify({'message': 'File stored successfully'}), 200
    else:
        return jsonify({'message': 'Failed to store the file'}), 500


# Distribue les messages
@app.route('/synchroniser', methods=['POST'])
def synchroniser():

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


@app.route('/synchronize_files', methods=['POST'])
def synchronize_files():
    # Extracting sender and message from request
    receiver = request.json['receiver']

    files = fichiers_collection.find({'receiver': receiver})

    synchronized_files = []

    # Ajouter chaque message à la liste synchronisée
    for file in files:
        sender = file['sender']
        receiver = file['receiver']
        filename = file['filename']
        file_data = file['file_data']
        timestamp = file['timestamp']
    
        file_data_base64 = base64.b64encode(file_data).decode('utf-8')

        synchronized_files.append({
            'sender': sender,
            'receiver': receiver,
            'filename': filename,
            'file_data': file_data_base64,
            'timestamp': timestamp
        })
    
    criteria = {'receiver': receiver}
    deleted_result = fichiers_collection.delete_many(criteria)
    print(f"Number of files deleted: {deleted_result.deleted_count}")

    return jsonify(synchronized_files), 200