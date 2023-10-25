def buy_route(data, addr, cur, con):
    from smodules.Buy import Buy
    return Buy(cur, addr, con, data)

def sell_route(data, addr, cur, con):
    from smodules.Sell import Sell
    return Sell(cur, con, data, addr)

def inventory_route(data, addr, cur):
    from smodules.Inventory import Inventory
    return Inventory(cur, data, addr)

def login_route(data, addr, cur, connected_clients):
    from smodules.Login import Login
    return Login(cur, data, addr, connected_clients)

def list_route(data, addr, cur):
    from smodules.List import List
    return List(cur, data, addr)

def balance_route(data, addr, cur):
    from smodules.Balance import Balance
    return Balance(cur, data, addr)

def lookup_route(data, addr, cur, con):
    from smodules.Lookup import Lookup
    return Lookup(cur, con, data, addr)

def deposit_route(data, addr, cur, con):
    from smodules.Deposit import Deposit
    return Deposit(cur, con, data, addr)

def handle_client(conn, addr, MAX_LINE, s, con, cur, connected_clients):
    print('s: Connected by', addr) # Print client address

    while True:
        data = conn.recv(MAX_LINE) # Receive data from client
        if not data: break # Break if no more data

        if data.decode().strip() == "SHUTDOWN":
            print('s: Received:', data.decode().strip())
            conn.sendall(b"200 OK|SHUTDOWN")
            return True

        if "QUIT" in data.decode():
            print('s: Received QUIT command from', addr)
            data = b"200 OK|QUIT"
        if "LOGIN" in data.decode():
            data = login_route(data, addr, cur, connected_clients)
            data = data.encode()
        if "BALANCE" in data.decode():
            data = balance_route(data, addr, cur)
            data = data.encode()
        if "BUY" in data.decode():
            data = buy_route(data, addr, cur, con)
            data = data.encode()
        if "INVENTORY"in data.decode():
            data = inventory_route(data, addr, cur)
            data = data.encode()
        if "SELL" in data.decode():
            data = sell_route(data, addr, cur, con)
            data = data.encode()
        if "LIST" in data.decode():
            data = list_route(data, addr, cur)
            data = data.encode()
        if "STATUS" in data.decode():
            #  - SEND BACK "SERVER_RUNNING"
            data = f"200 OK|SERVER_RUNNING"
            data = data.encode()
        if "LOGOUT" in data.decode():
            print('s: Received LOGOUT command from', addr)
            for client in connected_clients:
                if client[1] == addr:
                    client[0] = "anonymous"
            data = f"200 OK"
            data = data.encode()
        if "WHO" in data.decode():
            data = f"200 OK|{connected_clients}"
            data = data.encode()
        if "LOOKUP" in data.decode():
            data = lookup_route(data, addr, cur, con)
            data = data.encode()
        if "DEPOSIT" in data.decode():
            data = deposit_route(data, addr, cur, con)
            data = data.encode()
        conn.sendall(data) # Send data back to client

    # Close the connection
    conn.close()
    
__all__ = ["handle_client"]