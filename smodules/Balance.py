def Balance(cur, data, addr):
    print('s: Received', repr(data), 'from', addr)
    #  - GRAB OWNER ID FROM CLIENT REQUEST
    owner_id = data.decode().split(" ")[1]
    # - GRAB THE BALANCE OF THE USER
    # - clear cur object
    cur.execute(f"SELECT usd_balance FROM Users WHERE ID = {owner_id}")
    balance = cur.fetchall()
    return str(balance)
    
__all__ = ["Balance"]