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
        print('s: Connected by', addr) # Print client address

        while True:
            data = conn.recv(MAX_LINE) # Receive data from client
            if not data: break # Break if no more data

            if data.decode().strip() == "SHUTDOWN":
                print('s: Received:', data.decode().strip())
                conn.sendall(b"200 OK\n")
                conn.close()
                s.close()
                con.close() # Close the database connection
                exit() # Terminate the server

            if "QUIT" in data.decode():
                print('s: Received QUIT command from', addr)
                #   - Send confirmation message back to client
                data = b"200 OK"

            if "QUERY" in data.decode():
                print('s: Received', repr(data), 'from', addr)
                
                #  - GET CARD DATA
                card_name = data.decode().split(" ")[1]
                cur.execute("SELECT * FROM Pokemon_cards WHERE card_name = ? AND owner_id IS NULL", (card_name,))
                results = cur.fetchall()
                
                #  - SEND CARD DATA OR ERROR MESSAGE
                if len(results) == 0:
                    data = b"s: Error 403: Card does not exist."
                else:
                    data = str(results[0]).encode()
            if "LOGIN" in data.decode():
                print('s: Received', repr(data), 'from', addr)
                #  - GET USERNAME AND PASSWORD
                username = data.decode().split(" ")[1]
                password = data.decode().split(" ")[2].replace("\n", "")
                
                #  - CHECK IF USERNAME AND PASSWORD ARE CORRECT
                cur.execute("SELECT * FROM Users WHERE user_name = ? AND password = ?", (username, password))
                results = cur.fetchall()
                if len(results) == 0:
                    server_response = b"s: Error 403: Wrong UserID or Password"
                    filler_list = [0,1]
                    data = f"{server_response}{filler_list}".encode()
                else:
                    #  - SEND USER DATA
                    server_response = b"s: 200: OK|"
                    user_data = str(results[0]).encode()
                    print(user_data)
                    data = f"{server_response}{user_data}".encode()
            if "BALANCE" in data.decode():
                print('s: Received', repr(data), 'from', addr)
                #  - GRAB OWNER ID FROM CLIENT REQUEST
                owner_id = data.decode().split(" ")[1]
                # - GRAB THE BALANCE OF THE USER
                # - clear cur object
                cur.execute(f"SELECT usd_balance FROM Users WHERE ID = {owner_id}")
                balance = cur.fetchall()
                data = str(balance).encode()
            if "BUY" in data.decode():
                data = buy_route(data)
                data = data.encode()
            if "INVENTORY"in data.decode():
                data = inventory_route(data, addr)
                data = data.encode()
            if "SELL" in data.decode():
                data = sell_route(data, addr)
                data = data.encode()
            if "LIST" in data.decode():
                print('s: Received', repr(data), 'from', addr)
                #  - GRAB OWNER ID FROM CLIENT REQUEST
                user_name = data.decode().split(" ")[1]
                if user_name == "Root":
                    #  - GRAB ALL CARD DATA WHERE OWNER ID is NULL
                    cur.execute("SELECT * FROM Pokemon_cards")
                else:
                    #  - QUERY FOR USER_ID FROM USER_NAME
                    cur.execute("SELECT ID FROM Users WHERE user_name = ?", (user_name,))
                    owner_id = cur.fetchall()[0][0]
                    #  - GRAB ALL CARD DATA WHERE OWNER ID = OWNER ID
                    cur.execute("SELECT * FROM Pokemon_cards WHERE owner_id = ?", (owner_id,))
                results = cur.fetchall()
                #  - SEND CARD DATA
                data = f"200 OK|{str(results)}".encode()
            if "STATUS" in data.decode():
                #  - SEND BACK "SERVER_RUNNING"
                data = b"SERVER_RUNNING"
                data = str(data).encode()
            conn.sendall(data) # Send data back to client

        # Close the connection
        conn.close()

def buy_route(data):
    global cur, con 
    from smodules.Buy import Buy
    return Buy(cur, con, data)

def sell_route(data, addr):
    global cur, con
    from smodules.Sell import Sell
    return Sell(cur, con, data, addr)

def inventory_route(data, addr):
    global cur, con
    from smodules.Inventory import Inventory
    return Inventory(cur, con, data, addr)

main()