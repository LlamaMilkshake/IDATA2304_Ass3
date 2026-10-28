# Generic TCP client boilerplate structure:
# def create_client_socket():
# def connect_to_server():
# def receive_data():
# def read_send_command():


import socket
import sys

def create_client_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server(sock, host, port):
    sock.connect((host, port))

def receive_data(sock):
    return sock.recv(1024)

def read_send_command(sock):
    while True:
        command = input("Remote>>")
        if command == '':
            '\n'
        else:
            sock.sendall((command).encode())
            response = sock.recv(1024).decode().strip()
            print(response)

        if command.upper() == 'QUIT':
            break

def main():
    socket = create_client_socket()

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        print('Cannot run without server TCP port and hostname/IP address')
        return
    if len(sys.argv) > 2:
        host = sys.argv[2]
    else:
        print('Cannot run without server hostname/IP address')
        return


    try:
        connect_to_server(socket, host, port)
        response = receive_data(socket)
        print(response.decode(errors = 'ignore'))
        read_send_command(socket)
    except Exception as e:
        print(f'Could not reach server: {e}')
    finally:
        socket.close()

if __name__ == "__main__":
    main()