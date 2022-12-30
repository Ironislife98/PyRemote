import socket

HEADER: int = 64
PORT: int = 5050
SERVER: str = "127.0.0.1"
ADDR: tuple[str, int] = (SERVER, PORT)
FORMAT: str = "utf-8"
DISCONNECTED_MESSAGE: str = "DISCONNECT"


def send(msg: str):
    msg_length = len(msg)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b" " * (HEADER - len(msg_length))
    conn.send(msg_length)
    conn.send(msg.encode(FORMAT))


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(ADDR)

while True:
    command = input("Enter Command: ")
    send(command)
    if command == "logs":
        logs = []
        numLogs = int(conn.recv(1024).decode(FORMAT))
        for log in range(numLogs):
            size = int(conn.recv(HEADER).decode(FORMAT))
            logs.append(conn.recv(size).decode(FORMAT))
        print(len(logs))