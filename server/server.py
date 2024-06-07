import socket
import os
import threading



def handle_client(client_socket, client_address):
    # Handle client requests
    while True:
        data = client_socket.recv(2048).decode()
        if not data:
            break
        parts = data.split()
        command = parts[0].lower()
        filename = parts[1]

        if command == "read":
            try:
                with open(filename, "rb") as f:
                    filedata = f.read()
                client_socket.sendall(filedata)
            except FileNotFoundError:
                client_socket.sendall(b"Error: File not found.")
        elif command == "write":
            filedata = client_socket.recv(2048)
            with open(filename, "ab") as f:
                f.write(filedata)
            client_socket.sendall(b"Success: File written.")
        elif command == "create":
            try:
                with open(filename, "x"):
                    pass
                client_socket.sendall(b"Success: File created.")
            except FileExistsError:
                client_socket.sendall(b"Error: File already exists.")
        elif command == "delete":
            try:
                os.remove(filename)
                client_socket.sendall(b"Success: File deleted.")
            except FileNotFoundError:
                client_socket.sendall(b"Error: File not found.")
        else:
            client_socket.sendall(b"Error: Invalid command.")


    # Clean up
    client_socket.close()
    print(f"Connection closed with {client_address}")

def run_server():
    # Set up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = socket.gethostbyname(socket.gethostname())
    server_address = (server, 5050)
    server_socket.bind(server_address)
    server_socket.listen()
    print("Server is listening on", server_address)

    while True:
        # Accept client connections
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from", client_address)
        # Create a new thread or process to handle the client request
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == '__main__':
    run_server()
