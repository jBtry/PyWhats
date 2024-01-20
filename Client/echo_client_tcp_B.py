import socket
import threading


def receive_messages(ClientSocket):
    while True:
        try:
            Response = ClientSocket.recv(1024)
            print('\n')
            print(Response.decode('utf-8'))
        except socket.error as e:
            print(str(e))
            break

def send_messages(ClientSocket):
    while True:
        recipient = input('Enter recipient: ')
        message = input('Say Something: ')
        data = f'{recipient}:{message}'
        ClientSocket.send(str.encode(data))


ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

ClientName = input('Type your username: ')
ClientSocket.send(str.encode(ClientName))

while True:
    receive_thread = threading.Thread(target=receive_messages, args=(ClientSocket,))
    send_thread = threading.Thread(target=send_messages, args=(ClientSocket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

ClientSocket.close()
