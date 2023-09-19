import socket

# Define server address and port
SERVER_HOST = 'localhost'
SERVER_PORT = 4895

MAX_LINE = 256 # Maximum number of bytes to receive

# Client socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
s.connect((SERVER_HOST, SERVER_PORT)) # Connect to server address

# Send data
s.sendall(b'Hello, world') # Send data to server

# Receive data
data = s.recv(MAX_LINE) # Receive data from server

# Close the connection
s.close()

# Print received data
print('Received', repr(data)) # Print received data
