# Generic TCP server boilerplate structure:
# def create_socket():
# def bind_socket():
# def listen_for_connection():
# def accept_connection():
# def close_socket():

# Reusable receive_command pattern:
# recv
# decode
# strip

# Reusable main loop shape:
# accept
# loop{receive -> handle -> respond}
# close

# Reusable idea:
# separate handle_command(command) func that takes a string and returns a string
# (this maps well onto "design an application-layer protocol")

import socket
import sys
import threading
from handler import handle_command, get_channel


tv_lock = threading.Lock()        # protects all TV state
clients = set()                   # currently connected sockets
clients_lock = threading.Lock()   # protects the set above


def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def bind_socket(sock, host, port):
    sock.bind((host, port))

def listen_for_connection(sock):
    sock.listen()
    print(f'Server listening on {sock.getsockname()}')

def accept_connection(sock):
    return sock.accept()

def receive_command(conn_sock):
    try:
        data = conn_sock.recv(1024)             # receiver pausing code. Max message capacity 1024 bytes 
        if not data:
            return None
        return data.decode().strip()            # strip() removes empty space and \n before and after word. not in middle
    except Exception as e:
        print(f'Receive error: {e}')            # debugging
        return 'ERROR: communication failure'   # response sent to client

def close_socket(sock):
    sock.close()
    print('A socket closed: ')

def broadcast(message, exclude=None):
    """Send message to every connected remote except `exclude`."""
    with clients_lock:
        targets = [c for c in clients if c is not exclude]   # snapshot
    for c in targets:
        try:
            c.sendall(message.encode())
        except Exception as e:
            print(f'Broadcast failed for one client: {e}')   # its own thread cleans it up


def handle_client(conn_socket, addr):
    with clients_lock:
        clients.add(conn_socket)
    try:
        while True:
            command = receive_command(conn_socket)
            if not command or command.upper() == 'QUIT':
                conn_socket.sendall(b'Au revoiare!\n')
                break

            with tv_lock:
                before = get_channel()
                response = handle_command(command)
                after = get_channel()

            conn_socket.sendall((response + '\n').encode())
            if before != after:
                print(f'[STATE] Channel changed {before} -> {after}')
                broadcast(f'[NOTIFY] Channel changed {before} -> {after}\n', exclude=conn_socket)
    except Exception as e:
        print(f'Server error: {e}')
    finally:
        with clients_lock:
            clients.discard(conn_socket)
        close_socket(conn_socket)
        print('Connection socket to remote closed')


def main():
    host = '127.0.0.1'
    std_port = 1238
    port = int(sys.argv[1]) if len(sys.argv) > 1 else std_port

    server_socket = create_socket()
    bind_socket(server_socket, host, port)
    listen_for_connection(server_socket)
    server_socket.settimeout(1.0)       # lets Ctrl+C work on Windows

    try:
        while True:
            try:
                conn_socket, addr = accept_connection(server_socket)
            except socket.timeout:
                continue                # nobody connected this second, keep waiting

            conn_socket.settimeout(None)
            print(f'Server connected with: {addr}')
            try:
                conn_socket.sendall(b'You are now the TV captain. Type "quit" to disconnect.\n')
            except Exception as e:
                print(f'Server error: {e}')
                close_socket(conn_socket)
                continue

            threading.Thread(target=handle_client,
                             args=(conn_socket, addr),
                             daemon=True).start()
    except KeyboardInterrupt:
        print('\nServer shutting down')
    finally:
        close_socket(server_socket)


if __name__ == "__main__":
    main()
