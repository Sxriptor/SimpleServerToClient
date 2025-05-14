import os

# Folder to receive files from server
CLIENT_RECEIVED_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "received_client")

# Folder to receive files from client
SERVER_RECEIVED_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "received_server")

# Create the folders if they don't exist
os.makedirs(CLIENT_RECEIVED_DIR, exist_ok=True)
os.makedirs(SERVER_RECEIVED_DIR, exist_ok=True)
