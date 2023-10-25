def Inventory(cur, data, addr):
    try:
        print('s: Received', repr(data), 'from', addr)
                    
        #  - GET CARD DATA
        card_name = data.decode().split(" ")[1]
        userID = int(data.decode().split(" ")[2])
        pokemon = cur.execute(f"SELECT card_name, count FROM Pokemon_cards WHERE owner_id = {userID} AND card_name = '{card_name}'").fetchall()
        # - GRAB A CARD AT A SPECIFIC USER 
        if (pokemon == []):
            data = b"404 NOT FOUND"
        else:
            data = f"200 OK|{pokemon[0][0]} {pokemon[0][1]}"
        return data
    except Exception as e:
        print(f"s: An error occurred: {e}")
        return "500 Internal Server Error"
        
__all__ = ["Inventory"]