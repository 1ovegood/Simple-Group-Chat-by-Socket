import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from queue import Queue, Empty
 
class ChatClient:
    """Initializes the ChatClient.""" 
    def __init__(self, protocol):
        self.protocol = protocol
        """Initializes the GUI."""
        self.username = ""
        self.client_socket = None
        self.message_queue = Queue()  
         
         
        self.bg_color = "#f0f0f0"
        self.fg_color = "#333333"
        self.button_color = "#4CAF50"
        self.entry_color = "#ffffff"
         
         
        self.login_window = tk.Tk()
        self.login_window.title("Login")
        self.login_window.configure(bg=self.bg_color)
         
        self.username_label = tk.Label(self.login_window, text="Username:", bg=self.bg_color, fg=self.fg_color)
        self.username_label.pack(pady=10)
 
        self.username_entry = tk.Entry(self.login_window, bg=self.entry_color, fg=self.fg_color, font=("Arial", 14))
        self.username_entry.pack(pady=10)

        self.login_button = tk.Button(self.login_window, text="Login", command=self.login, bg=self.button_color, fg="#ffffff")
        self.login_button.pack(pady=10)
 
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_closing_login)
 
    def login(self):
        """Handles the login process, including connecting to the server."""
        self.username = self.username_entry.get()
        if not self.username:
            messagebox.showerror("Error", "Please enter a username.")
        self.login_window.destroy() 
        self.start_chat_window()     
        server_address = ('127.0.0.1', 1234)      # Change this to the IP address of the server.

        """Initializes the chat client with the specified protocol."""
        if self.protocol == "TCP":
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(server_address)
        elif self.protocol == "UDP":
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
         
        self.client_socket.sendall(self.username.encode())
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.process_messages()  
 
    def start_chat_window(self):
        """Initializes the GUI after login."""
        self.chat_window = tk.Tk()
        self.chat_window.title("Chat Room")
        self.chat_window.configure(bg=self.bg_color)
 
        self.chat_area = scrolledtext.ScrolledText(self.chat_window, state='disabled', bg=self.entry_color, fg=self.fg_color, font=("Arial", 12), wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
 
        self.message_entry = tk.Entry(self.chat_window, bg=self.entry_color, fg=self.fg_color, font=("Arial", 14))
        self.message_entry.pack(padx=10, pady=10, fill=tk.X, expand=True)
 
        self.send_button = tk.Button(self.chat_window, text="Send", command=self.send_message, bg=self.button_color, fg="#ffffff")
        self.send_button.pack(pady=10)
 
        self.chat_window.protocol("WM_DELETE_WINDOW", self.on_closing_chat)
 
    def send_message(self):
        """Sends a message to the server."""
        message = self.message_entry.get()
        if message:
            if self.protocol == "TCP":
                self.client_socket.sendall(message.encode())
            elif self.protocol == "UDP":
                self.client_socket.sendto(message.encode(), ('127.0.0.1', 1234))
            self.message_entry.delete(0, tk.END)
 
    def receive_messages(self):
        """Receives messages from the server and adds them to the queue."""
        while True:
            try:
                if self.protocol == "TCP":
                    data = self.client_socket.recv(1024)
                elif self.protocol == "UDP":
                    data, _ = self.client_socket.recvfrom(1024)
 
                if data:
                    self.message_queue.put(data.decode())  
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
 
    def process_messages(self):
        """Processes messages from the queue and updates the chat area."""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.update_chat_area(message)
        except Empty:
            pass
        self.chat_window.after(100, self.process_messages)  
 
    def update_chat_area(self, message):
        """Updates the chat area with a new message."""
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)
 
    def on_closing_login(self):
        """Handles the closing event of the login window."""
        self.login_window.destroy()
 
    def on_closing_chat(self):
        """Handles the closing event of the chat window and closes the socket."""
        if self.client_socket:
            self.client_socket.close()
        self.chat_window.destroy()
 
    def run(self):
        """Starts the main event loop of the application."""
        self.login_window.mainloop()
 
if __name__ == "__main__":
    protocol = input("Type the protocol (TCP/UDP): ")
    protocol = protocol.upper()
    chat_client = ChatClient(protocol)
    chat_client.run()
