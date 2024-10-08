# Simple Chat Application

This repository contains a simple chat application implemented in Python using sockets for network communication and tkinter for the GUI. The application supports both TCP and UDP protocols.

## Features

- **TCP/UDP Support**: Users can choose between TCP or UDP protocol for message exchange.
- **Multi-threaded Server**: Handles multiple client connections simultaneously.
- **GUI Client**: A simple and intuitive graphical user interface for interacting with the chat server.

## Structure

The project consists of two main parts:

1. **Server**: Handles incoming connections, receives messages from clients, and broadcasts them to all connected clients.
2. **Client**: Connects to the server, sends messages, and displays received messages in a GUI.

## Getting Started

### Prerequisites

- Python 3.x
- tkinter library (usually comes with Python)

### Running the Server

1. Navigate to the directory.
2. Run the following command in your terminal:
   ```bash
   python socket_server.py
3. Open another terminal and run:
   ```bash
   python socket_client.py
4.You can change server address to your own server if you like:


## Usage
After launching both the server and the client:
1.Log in with a username.
2.Start sending and receiving messages.

