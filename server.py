import socket

# Define server port
PORT = 4895 # Port number is a 16-bit unsigned integer
MAX_PENDING = 5 # Maximum number of pending connections
MAX_LINE = 256 # Maximum number of bytes to receive

# Passive open
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
s.bind(('', PORT)) # Bind the socket to the port
s.listen(MAX_PENDING) # Listen for connection
# Print to notify user that server is ready
print('Server listening on port', PORT)

# Wait for connection
while True:
    conn, addr = s.accept() # Accept a connection
    print('Connected by', addr) # Print client address

    # Receive data and send it back
    while True:
        data = conn.recv(MAX_LINE) # Receive data from client
        if not data: break # Break if no more data
        conn.sendall(data) # Send data back to client

    # Close the connection
    conn.close()
    