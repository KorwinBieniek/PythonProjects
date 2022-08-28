import threading
import socket

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!quit"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()

client_usernames = []


def handle_client(conn, addr):
    client_username = addr
    print(f"[NEW CONNECTION] {client_username} Connected")

    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if str(msg) == '!who':
                users = '\n'.join(client_usernames)
                for c in clients:
                    c.sendall(f"List of current users:\n{users}".encode(FORMAT))
            if str(msg).startswith('!username'):
                print(client_usernames)
                if msg[len('!username') + 1:] in client_usernames:
                    with clients_lock:
                        for c in clients:
                            c.sendall(f"username '{msg[len('!username') + 1:]}': has been already taken."
                                      f"Change your username by typing !username 'your_username'".encode(FORMAT))
                    client_username = addr
                else:
                    client_username = msg[len('!username') + 1:]
                    client_usernames.append(client_username)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                client_usernames.remove(client_username)
                connected = False

            print(f"[{client_username}]: {msg}")
            with clients_lock:
                for c in clients:
                    c.sendall(f"[{client_username}]: {msg}".encode(FORMAT))

    finally:
        with clients_lock:
            clients.remove(conn)

        conn.close()


def start():
    print('[SERVER STARTED]!')
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start()
