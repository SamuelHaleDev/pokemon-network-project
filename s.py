import socket
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import threading
import queue

# Define server port
PORT = 4988 # Port number is a 16-bit unsigned integer
MAX_PENDING = 5 # Maximum number of pending connections
MAX_LINE = 256 # Maximum number of bytes to receive
connected_clients = []
connection_pool = queue.Queue(maxsize=MAX_PENDING)
SHUTDOWN = False
exit_event = threading.Event()


clients_lock = threading.Lock()

# Passive open
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
s.bind(('', PORT)) # Bind the socket to the port
s.listen(MAX_PENDING) # Listen for connection

def main():
    global connected_clients
    try:
        while not SHUTDOWN:
            with ThreadPoolExecutor(max_workers=MAX_PENDING) as executor:
                conn, addr = s.accept() # Accept a connection
                
                executor.submit(handle_client_route, conn, addr, exit_event, connected_clients)
                if exit_event.is_set():
                    break
        executor.shutdown(wait=True)
        s.close()
    except Exception as e:
        print(f"s: An error occurred: {e}")
        print("s: Server shutting down.")
        executor.shutdown(wait=True)
        s.close()
        
    
            
def create_connection():
    return sqlite3.connect("Pokemon.db")

def get_connection():
    global MAX_PENDING, connection_pool
    with clients_lock:
        if connection_pool.qsize() < MAX_PENDING:
            connection_pool.put(create_connection())
        return connection_pool.get()

def handle_client_route(conn, addr, exit_event, connected_clients):
    global MAX_LINE, s, SHUTDOWN
    con = get_connection()
    cur = con.cursor()
    with clients_lock:
        connected_clients.append(["anonymous", addr])
        print(f"s: New connection from {addr}. {len(connected_clients)} connected clients.")
    from smodules.Client import handle_client
    finished = handle_client(conn, addr, MAX_LINE, s, con, cur, connected_clients)
    
    if finished:
        with clients_lock:
            for client in connected_clients:
                if client[1] == addr:
                    connected_clients.remove(client)
            print(f"s: Connection from {addr} closed. {len(connected_clients)} connected clients.")
            SHUTDOWN = True
        cur.close()
        con.close()
        conn.close()
        exit_event.set()
        return
            
        

main()