import socket
 
def start_server(protocal):
    """
    Initializes a socket server based on the specified protocol (TCP or UDP). 
    Listens for incoming connections or messages and responds accordingly.
    """
    if protocal == "TCP":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', 1234)       # your expected server address and port
        server_socket.bind(server_address)
        server_socket.listen()
        print("TCP server started, waiting for connection...")
        while True:
            connection, client_address = server_socket.accept()
            print(f"received connection from {client_address}")
            while True:
                data = connection.recv(1024) 
                if data:
                    print(f"received : {data.decode()}")
                    response = input("Reply: ")  
                    connection.sendall(response.encode())  
                else:
                    break
             
    elif protocal == "UDP":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('127.0.0.1', 1234) 
        server_socket.bind(server_address)
        print("UDP server started, waiting for message...")
        while True:
            data, client_address = server_socket.recvfrom(1024)
            print(f"{client_address}  Send: {data.decode()}")
            response = input("Reply: ")
            server_socket.sendto(response.encode(), client_address)
 
    else:
        print("Wrong protocal type!")
        return
    connection.close() 
 
 
 
if __name__ == "__main__":
    """
    Main entry point of the server script. Prompts user for protocol type and
    initiates the server based on input.
    """
    protocal = input("type the protocal (TCP/UDP): ")
    protocal = protocal.upper()
    start_server(protocal)