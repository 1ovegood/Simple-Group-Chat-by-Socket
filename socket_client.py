import socket

def start_client(protocal):
    """
    Initializes a TCP socket connection if the protocol is TCP,
    or a UDP socket connection if the protocol is UDP.
    """
    if protocal == "TCP":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', 1234)
        client_socket.connect(server_address)
        while True:
            message = input("Send: ")  
            client_socket.sendall(message.encode())  
             
            data = client_socket.recv(1024)  
            print(f"Received: {data.decode()}")
   
    elif protocal == "UDP":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('127.0.0.1', 1234)    # corresponding server address and port
        while True:
            message = input("Send: ")  
            client_socket.sendto(message.encode(), server_address)  
             
            data, server = client_socket.recvfrom(1024)  
            print(f"Received from {server}: {data.decode()}")
          
    else:
        print("wrong protocal")
        return
 

    client_socket.close() 

"""
Main entry point of the script. Prompts the user for a protocol type
and starts the client with the specified protocol.
"""
if __name__ == "__main__":

    protocal = input("type the protocal (TCP/UDP): ")
    protocal = protocal.upper()
    start_client(protocal)