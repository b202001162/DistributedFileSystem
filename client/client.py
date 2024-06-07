import socket

def run_client():
    # Connect to the server
    server = input("Enter server address: ")
    server_address = (server, 5050)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    print("Connected to server:", server_address)

    # Send requests to the server
    while True:
        # Get user input for the requested operation
        command = input("Enter command (read, write, create, delete) or exit: ")
        if command.lower() == 'exit':
            break
        filename = input("Enter filename: ")
        # Send the command and filename to the server   
        client_socket.sendall(f"{command} {filename}".encode())
        # Process server response here
        if command.lower() == 'write':
            delimiter = '$'
            print(f"When you're done, enter '{delimiter}' on a new line: ")
            print("Enter file content below: ")
            buffer = []
            delimiter = "$"
            while True:
                print("> ", end="")
                line = input()
                if(line == delimiter):
                    break
                if (len(line) > 1):
                    if(line[-1] == delimiter):
                        line = line[:-1]  # Remove the delimiter '$' from the line
                        buffer.append(line)
                        break
                buffer.append(line)

            multiline_string = "\n".join(buffer)
            client_socket.sendall(multiline_string.encode())
        response = client_socket.recv(2048)
        if command.lower() == 'read':
            print(response.decode())
        else: 
            print(response.decode())

    # Clean up
    client_socket.close()

if __name__ == '__main__':
    run_client()
