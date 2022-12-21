import socket
import sys

HEADER = 64 
PORT = 5000
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECTED_MESSAGE = "DISCONNECT"


class Client:
    def __init__(self, address):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(address)

    def send(self, msg: str):
        msg_length = len(msg)
        msg_length = str(msg_length).encode(FORMAT)
        msg_length += b" " * (HEADER - len(msg_length))
        self.conn.send(msg_length)
        self.conn.send(msg.encode(FORMAT))
        print(self.conn.recv(1024))

    def disconnect(self):
        self.send(DISCONNECTED_MESSAGE)
        self.conn.close()
        sys.exit()


client = Client(ADDR)
client.send("cmd dir")

client.disconnect()
