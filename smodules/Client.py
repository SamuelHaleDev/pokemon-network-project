def buy_route(data):
    global cur, con 
    from smodules.Buy import Buy
    return Buy(cur, con, data)

def sell_route(data, addr):
    global cur, con
    from smodules.Sell import Sell
    return Sell(cur, con, data, addr)

def inventory_route(data, addr):
    global cur
    from smodules.Inventory import Inventory
    return Inventory(cur, data, addr)

def query_route(data, addr):
    global cur
    from smodules.Query import Query
    return Query(cur, data, addr)

def login_route(data, addr):
    global cur
    from smodules.Login import Login
    return Login(cur, data, addr)

def list_route(data, addr):
    global cur
    from smodules.List import List
    return List(cur, data, addr)

def balance_route(data, addr):
    global cur
    from smodules.Balance import Balance
    return Balance(cur, data, addr)

def lookup_route(data, addr):
    global cur
    from smodules.Lookup import Lookup
    return Lookup(cur, con, data, addr)

def deposit_route(data, addr):
    global cur
    from smodules.Deposit import Deposit
    return Deposit(cur, con, data, addr)

def handle_client(conn, addr, MAX_LINE, s, con, cur):
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
            data = query_route(data, addr)
            data = data.encode()
        if "LOGIN" in data.decode():
            data = login_route(data, addr)
            data = data.encode()
        if "BALANCE" in data.decode():
            data = balance_route(data, addr)
            data = data.encode()
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
            data = list_route(data, addr)
            data = data.encode()
        if "STATUS" in data.decode():
            #  - SEND BACK "SERVER_RUNNING"
            data = f"SERVER_RUNNING"
            data = data.encode()
        if "LOGOUT" in data.decode():
            print('s: Received LOGOUT command from', addr)
            data = f"200 OK"
            data = data.encode()
        if "WHO" in data.decode():
            data = f"200 OK"
            data = data.encode()
        if "LOOKUP" in data.decode():
            data = lookup_route(data, addr)
            data = data.encode()
        if "DEPOSIT" in data.decode():
            data = deposit_route(data, addr)
            data = data.encode()
        conn.sendall(data) # Send data back to client

    # Close the connection
    conn.close()
    
__all__ = ["handle_client"]