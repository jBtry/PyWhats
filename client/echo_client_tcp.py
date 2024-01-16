#!/usr/bin/env python3

import socket

if __name__ == '__main__':
    # Etape 1 : création de la socket cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Etape 1 suite : connexion
        s.connect(('localhost', 10101))
        while True:
            # lecture clavier d'une chaine
            st = input("Tapez une chaine (FIN pour arreter): ")
            # condition d'arrêt
            if st == "FIN":
                break
            # Etape 2 : émission de la chaine après encodage
            s.sendall(st.encode('utf-8'))
            # Etape 2 suite : réception de la chaine
            data = s.recv(1024)
            # décodage de la chaine
            st = data.decode('utf-8')
            # affichage de la chaine
            print('Received', st)

