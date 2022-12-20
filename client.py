import socket

HEADER = 64 
PORT = 5000
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECTED_MESSAGE = "DISCONNECT"


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((ADDR))

run = True
while run:
    msg = input("Message to send: ").encode(FORMAT)
    msg_length = len(msg)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b" " * (HEADER - len(msg_length))
    conn.send(msg_length)
    conn.send(msg)
    print(conn.recv(1024))