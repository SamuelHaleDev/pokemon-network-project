import socket
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import threading
import queue

# Define server port
PORT = 4987 # Port number is a 16-bit unsigned integer
MAX_PENDING = 5 # Maximum number of pending connections
MAX_LINE = 256 # Maximum number of bytes to receive
connected_clients = 0
connection_pool = queue.Queue(maxsize=MAX_PENDING)

clients_lock = threading.Lock()

# Passive open
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
s.bind(('', PORT)) # Bind the socket to the port
s.listen(MAX_PENDING) # Listen for connection

def main():
    with ThreadPoolExecutor(max_workers=MAX_PENDING) as executor:
        while True:
            conn, addr = s.accept() # Accept a connection
            
            executor.submit(handle_client_route, conn, addr)
            
def create_connection():
    return sqlite3.connect("Pokemon.db")

def get_connection():
    global MAX_PENDING, connection_pool
    with clients_lock:
        if connection_pool.qsize() < MAX_PENDING:
            connection_pool.put(create_connection())
        return connection_pool.get()

def handle_client_route(conn, addr):
    global connected_clients, MAX_LINE, s
    con = get_connection()
    cur = con.cursor()
    with clients_lock:
        connected_clients += 1
        print(f"s: New connection from {addr}. {connected_clients} connected clients.")
    from smodules.Client import handle_client
    handle_client(conn, addr, MAX_LINE, s, con, cur)
    
    with clients_lock:
        connected_clients -= 1
        print(f"s: Connection from {addr} closed. {connected_clients} connected clients.")

main()