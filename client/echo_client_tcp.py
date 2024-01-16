#!/usr/bin/env python3
import socket
import ssl

def do_encrypt(message):
    return message

if __name__ == '__main__':
    # Specify the path to the server's certificate file
    certfile = "server.crt"

    # Create the SSL/TLS context
    context = ssl.create_default_context(verify_mode=ssl.CERT_REQUIRED, cafile=certfile)

    # Create the socket and wrap it with SSL/TLS
    with socket.create_connection(('localhost', 10101)) as s:
        s = context.wrap_socket(s)

        while True:
            # Read a message from the user
            st = input("Tapez une chaine (FIN pour arreter): ")

            # If the message is "FIN", stop the loop
            if st == "FIN":
                break

            # Encode the message and send it to the server
            s.sendall(do_encrypt(st).encode('utf-8'))

            # Receive a response from the server and decode it
            data = s.recv(1024)
            st = data.decode('utf-8')

            # Print the response
            print('Received', st)