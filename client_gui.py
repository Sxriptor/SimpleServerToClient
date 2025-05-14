# client_gui.py
import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
from shared_constants import CLIENT_RECEIVED_DIR

HOST = '10.0.0.117'  # IP of the server
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def receive():
    while True:
        try:
            header = client_socket.recv(1024).decode()
            if header.startswith("FILE:"):
                _, filename, filesize = header.split(":")
                filepath = os.path.join(CLIENT_RECEIVED_DIR, filename)
                with open(filepath, "wb") as f:
                    remaining = int(filesize)
                    while remaining > 0:
                        data = client_socket.recv(min(4096, remaining))
                        if not data:
                            break
                        f.write(data)
                        remaining -= len(data)
                log_message(f"Received file: {filename} (saved to {filepath})")
                open_button.config(state=tk.NORMAL)
            else:
                log_message(f"Server: {header}")
        except:
            log_message("Connection lost.")
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

def open_folder():
    subprocess.Popen(f'explorer "{CLIENT_RECEIVED_DIR}"')

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

open_button = tk.Button(root, text="📂 Open Folder", command=open_folder, state=tk.DISABLED)
open_button.pack(side=tk.LEFT, padx=5)

threading.Thread(target=receive, daemon=True).start()
root.mainloop()
