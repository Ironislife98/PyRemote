import socket 
import threading
import os

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


def handleConnection(conn: socket, addr):
    print(f"{addr} has connected!")
    connected = True
    while connected:
        # Recieve the header, then decode the message using the length of the message
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECTED_MESSAGE:
                print(f"{addr} has disconnected!")
                clients.pop(clients.index(conn))
                connected = False
                break
            else:
                if msg[:3] == "cmd":
                    print(f"Remote system running command: {msg[3:]}")
                    print("Output: ", end="")
                    os.system(msg[3:])
            clients.append(conn)
            broadcast(msg)



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
