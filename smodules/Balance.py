def Balance(cur, data, addr):
    try:
        print('s: Received', repr(data), 'from', addr)
        #  - GRAB OWNER ID FROM CLIENT REQUEST
        owner_id = data.decode().split(" ")[1]
        # - GRAB THE BALANCE OF THE USER
        # - clear cur object
        cur.execute(f"SELECT usd_balance FROM Users WHERE ID = {owner_id}")
        balance = cur.fetchall()
        response = f"200 OK|{balance[0][0]}"
        return response
    except Exception as e:
        print(f"s: An error occurred: {e}")
        return "500 Internal Server Error"
    
__all__ = ["Balance"]