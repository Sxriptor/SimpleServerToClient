import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import os

SERVER_IP = '127.0.0.1'  # Change this to the server's IP on your network
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        log_message("Connected to server.")
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Connection Failed", f"Could not connect to server:\n{e}")

def receive_messages():
    while True:
        try:
            header = client_socket.recv(1024).decode()
            if header.startswith("FILE:"):
                _, filename, filesize = header.split(":")
                save_path = os.path.join("received_files", filename)
                os.makedirs("received_files", exist_ok=True)
                with open(save_path, "wb") as f:
                    remaining = int(filesize)
                    while remaining > 0:
                        data = client_socket.recv(min(4096, remaining))
                        if not data:
                            break
                        f.write(data)
                        remaining -= len(data)
                log_message(f"Received file: {filename} (saved to {save_path})")
            else:
                log_message(f"Server: {header}")
        except:
            log_message("Disconnected from server.")
            break

def send_message():
    msg = entry.get()
    if msg:
        try:
            client_socket.sendall(msg.encode())
            log_message(f"You: {msg}")
            entry.delete(0, tk.END)
        except:
            log_message("Failed to send message.")

def send_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        try:
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)
            client_socket.sendall(f"FILE:{filename}:{filesize}".encode())
            with open(filepath, "rb") as f:
                while (chunk := f.read(4096)):
                    client_socket.sendall(chunk)
            log_message(f"File sent: {filename}")
        except:
            log_message("Failed to send file.")

def log_message(msg):
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, msg + "\n")
    chat_log.config(state=tk.DISABLED)
    chat_log.see(tk.END)

# GUI Setup
root = tk.Tk()
root.title("Client Chat")

chat_log = tk.Text(root, state=tk.DISABLED, width=60, height=20)
chat_log.pack(padx=10, pady=5)

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=(10, 5), pady=5)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

file_button = tk.Button(root, text="Send File", command=send_file)
file_button.pack(side=tk.LEFT, padx=5)

# Start connection after GUI loads
root.after(100, connect_to_server)
root.mainloop()
