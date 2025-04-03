import socket

# Server setup
server = "0.0.0.0"  # Listen on all available network interfaces
port = 5555          # Port to listen on

# Create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
s.bind((server, port))

# Start listening for connections (max of 5 connections)
s.listen(5)
print(f"Server started, listening on {server}:{port}")

# Accept a client connection
conn, addr = s.accept()
print(f"Connected to {addr}")

# Send a welcome message to the client
conn.sendall("Welcome to the server!".encode())

# Close the connection
conn.close()