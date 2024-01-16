#!/usr/bin/env python3
import socket
from Crypto.Cipher import AES

def do_decrypt(ciphertext):
    obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    message = obj2.decrypt(ciphertext)
    return message

if __name__ == '__main__':
    # Etape 1 : création de la socket d'écoute
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ecoute:
        # Etape 1 suite : liaison de la socket d'écoute (choix du port)
        ecoute.bind(('', 10101))
        # Etape 2 : ouverture du service
        ecoute.listen()
        while True:
            # A METTRE DANS LE WITH PRECEDANT A LA SUITE DU listen
            # Etape 3 : attente et acceptation d'une nouvelle connexion
            service, addr = ecoute.accept()
            with service:
                while True:
                    # Etape 4 : réception d'au max 1024 octets
                    data = service.recv(1024)
                    do_decrypt(data)
                    # si le client a fermé la connexion on arrête la boucle
                    if not data:
                        break
                    # affichage des données reçues
                    print(data)
                    # Etape 4 suite : on renvoi les données au client (echo)
                    service.sendall(data)
                # Etape 5 : fermeture socket de service (automatiquement par le with service)
        # Etape 6 : fermeture de la socket d'écoute (automatiquement par le with ecoute)
