import socket
import sys
import GUI

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
        if msg == DISCONNECTED_MESSAGE:
            sys.exit()

    def disconnect(self):
        self.send(DISCONNECTED_MESSAGE)

    def screenshot(self):
        self.send("screenshot")
        recvheader = int(self.conn.recv(1024))
        screenshot = self.conn.recv(recvheader)
        return screenshot

    def capture(self):
        pass


client = Client(ADDR)

app = GUI.App(client)
app.mainloop()

client.disconnect()
