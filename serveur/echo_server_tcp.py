#!/usr/bin/env python3
import socket
import ssl

if __name__ == '__main__':
    # Specify the path to the certificate and key files
    certfile = "C:\Users\cleme\Documents\GitHub\PyWhats\serveur\server.crt"

    keyfile = "C:\Users\cleme\Documents\GitHub\PyWhats\serveur\server.key"

    # Create the SSL/TLS context
    context = ssl.create_default_context(certfile=certfile, keyfile=keyfile)

    # Create the socket and wrap it with SSL/TLS
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock = context.wrap_socket(sock, server_side=True)
        sock.bind(('localhost', 10101))
        sock.listen()

        while True:
            # Accept a connection from a client
            service, addr = sock.accept()

            # Create an SSL/TLS connection
            with context.wrap_socket(service, server_side=True) as ssl_sock:
                # Handle the client connection
                while True:
                    data = ssl_sock.recv(1024)
                    if not data:
                        break

                    print(data.decode('utf-8'))
                    ssl_sock.sendall(data)
