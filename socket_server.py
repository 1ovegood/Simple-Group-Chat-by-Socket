import socket
import threading
 
def handle_client(connection, client_address):
    """Handles interactions with a single client, receiving messages and broadcasting them."""
    print(f"Received connection from {client_address}")
    username = connection.recv(1024).decode()  
    print(f"{username} has joined the chat.")
     
    broadcast(f"{username} has joined the chat.")
 
    while True:
        data = connection.recv(1024)
        if data:
            message = data.decode()
            print(f"{username}: {message}")
            broadcast(f"{username}: {message}")  
        else:
            break
 
    print(f"{username} has left the chat.")
    broadcast(f"{username} has left the chat.") 
    connection.close()
 
def broadcast(message):
    """Broadcast a message to all connected clients."""
    for client in clients:
        try:
            client.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message to client: {e}")
 
def start_server(protocol):
    """Starts the server in the specified protocol mode (TCP or UDP)."""
    if protocol == "TCP":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', 1234)          # server address and port
        server_socket.bind(server_address)
        server_socket.listen()
        print("TCP server started, waiting for connections...")

        """start catching massages from clients"""    
        while True:
            connection, client_address = server_socket.accept()
            clients.append(connection)
            threading.Thread(target=handle_client, args=(connection, client_address)).start()
 
    elif protocol == "UDP":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('127.0.0.1', 1234)
        server_socket.bind(server_address)
        print("UDP server started, waiting for messages...")
         
        """start catching massages from clients"""  
        while True:
            data, client_address = server_socket.recvfrom(1024)
            print(f"{client_address} Send: {data.decode()}")
            response = input("Reply: ")
            server_socket.sendto(response.encode(), client_address)
 
    else:
        print("Wrong protocol type!")
        return
 
if __name__ == "__main__":
    """Main entry point for the server script, initializes client list and starts the server."""
    clients = []
    protocol = input("Type the protocol (TCP/UDP): ")
    protocol = protocol.upper()
    start_server(protocol)
