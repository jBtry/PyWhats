import socket

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

# Response = ClientSocket.recv(1024)

# Demander le nom du client
ClientName = input('Type your username: ')
ClientSocket.send(str.encode(ClientName))

while True:
    # recipient = input('Enter recipient: ')
    # message = input('Say Something: ')
    
    # # Envoyer le message au format "recipient: message"
    # data = f'{recipient}:{message}'
    # ClientSocket.send(str.encode(data))
    
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()
