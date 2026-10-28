# Generic TCP client boilerplate structure:
# def create_client_socket():
# def connect_to_server():
# def receive_data():
# def read_send_command():


import socket
import sys
import threading


def create_client_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server(sock, host, port):
    sock.connect((host, port))

def receive_loop(sock):
    """Runs in its own thread: print whatever the server sends, whenever it arrives."""
    while True:
        try:
            data = sock.recv(1024)
        except OSError:
            break
        if not data:
            print('Server closed the connection')
            break
        print(data.decode(errors='ignore').strip())


def send_loop(sock):
    while True:
        command = input('Remote>> ')
        if command.strip() == '':
            continue
        try:
            sock.sendall(command.encode())
        except OSError:
            print('Connection lost')
            break
        if command.upper() == 'QUIT':
            break


def main():
    if len(sys.argv) < 3:
        print('Usage: client.py <port> <host>')
        return
    port = int(sys.argv[1])
    host = sys.argv[2]

    sock = create_client_socket()
    try:
        connect_to_server(sock, host, port)
        receiver = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
        receiver.start()
        send_loop(sock)
        receiver.join(timeout=2)    # let the goodbye message print
    except Exception as e:
        print(f'Could not reach server: {e}')
    finally:
        sock.close()

if __name__ == "__main__":
    main()