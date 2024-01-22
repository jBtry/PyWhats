import requests

class Client:
    def __init__(self):
        self.base_url = 'http://localhost:5000'

    def welcome(self):
        response = requests.get(f'{self.base_url}/welcome')
        welcome_message = response.json()
        return welcome_message

    def login(self, username, password):
        data = {'username': username, 'password': password}
        response = requests.post(f'{self.base_url}/login', json=data)
        return response

    def create_account(self, username, password):
        data = {'username': username, 'password': password}
        response = requests.post(f'{self.base_url}/create_account', json=data)
        return response
    
    def send_message(self, sender, receiver, message):
        data = {'sender': sender, 'receiver': receiver, 'message': message}
        response = requests.post(f'{self.base_url}/send_message', json=data)
        return response
    
    def get_messages(self, user):
        response = requests.get(f'{self.base_url}/get_messages/{user}')
        return response

    # ... (les autres méthodes restent inchangées)

if __name__ == '__main__':
    client = Client()

    welcome_message = client.welcome()
    print(welcome_message['message'])
    print("\n".join(welcome_message['options']))

    choice = input("Choisissez une option (1 ou 2): ")
    
    if choice == '1':
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        login_response = client.login(username, password)
        if login_response.status_code == 200:
            print('Authentification réussie')

            messages_response = client.get_messages(username)
            if messages_response.status_code == 200:
                messages = messages_response.json()
                print("Messages reçus :")
                for msg in messages:
                    print(f"De {msg['sender']}: {msg['message']}")

            while True:
                action = input("Que voulez-vous faire? (1: Envoyer un message, 2: Quitter) : ")
                if action == '1':
                    receiver = input("Entrer le nom d'utilisateur du destinataire : ")
                    message = input("Entrer votre message : ")
                    send_response = client.send_message(username, receiver, message)
                    if send_response.status_code == 200:
                        print("Message envoyé.")
                    else:
                        print("Erreur lors de l'envoi du message.")
                elif action == '2':
                    break

        else:
            print('Échec de l\'authentification')
    elif choice == '2':
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        create_account_response = client.create_account(username, password)
        if create_account_response.status_code == 201:
            print('Compte créé avec succès')

        else:
            print('Échec de la création du compte')
    else:
        print('Option invalide')
