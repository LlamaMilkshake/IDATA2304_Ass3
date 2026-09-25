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
from handler import handle_command


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


def main():
    host = '127.0.0.1'
    std_port = 1238
    server_socket = create_socket()

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = std_port
    
    bind_socket(server_socket, host, port)
    listen_for_connection(server_socket)

    while True:
        try:    # runs commands ONCE
            conn_socket, addr = accept_connection(server_socket)
            print(f'Server connected with: {addr}')
            conn_socket.sendall(b'You are now the TV captain. Type "quit" to disconnect.\n')
            while True:
                command = receive_command(conn_socket)
                if not command or command.upper() == 'QUIT':
                    conn_socket.sendall(b'Au revoiare!\n')
                    break
                response = handle_command(command)
                conn_socket.sendall((response).encode())
        except Exception as e:
            print(f'Server error: {e}')
        finally:
            if conn_socket:
                close_socket(conn_socket)
                print('Connection socket to remote closed')



if __name__ == "__main__":
    main()
