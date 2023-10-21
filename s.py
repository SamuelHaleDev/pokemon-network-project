import socket
import sqlite3

con = sqlite3.connect("Pokemon.db") # Connect to database

cur = con.cursor() # Create cursor object

# Define server port
PORT = 4898 # Port number is a 16-bit unsigned integer
MAX_PENDING = 5 # Maximum number of pending connections
MAX_LINE = 256 # Maximum number of bytes to receive

# Passive open
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
s.bind(('', PORT)) # Bind the socket to the port
s.listen(MAX_PENDING) # Listen for connection

def main():
    while True:
        conn, addr = s.accept() # Accept a connection

def handle_client_route(conn, addr):
    from smodules.Client import handle_client
    handle_client(conn, addr, MAX_LINE, s, con, cur)

main()