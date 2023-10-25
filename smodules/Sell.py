def Sell(cur, con, data, addr):
    try:
        print('s: Received', repr(data), 'from', addr)
        # - GET THE DATA FOR SELL
        #data = "SELL " + pokemon + " " + quantity + " " + price + " " + userID
        pokemon = data.decode().split(" ")[1]
        soldQuantity = data.decode().split(" ")[2]
        price = data.decode().split(" ")[3]
        userID = data.decode().split(" ")[4]
        print(pokemon + " " + soldQuantity + " " + price + " " + userID)
        cur.execute("SELECT count FROM Pokemon_cards WHERE card_name = ? AND owner_id = ?", (pokemon, userID))
        ownedQuantity = cur.fetchall()
        if (int(ownedQuantity[0][0]) == int(soldQuantity)):
            cur.execute(f"UPDATE Pokemon_cards SET count = count + {soldQuantity} WHERE owner_id IS NULL AND card_name = '{pokemon}'")
            cur.execute(f"DELETE FROM Pokemon_cards WHERE owner_id = {userID} AND card_name = '{pokemon}'")
        else: 
            #  - ADJUST THE AMOUNT OF CARDS THE OWNER STILL HAS AND CREATE OR UPDATE THE CARD WITH NULL OWNERID 
            cur.execute(f"UPDATE Pokemon_cards SET count = (count - {soldQuantity}) WHERE owner_id = {userID} AND card_name = '{pokemon}'")
            cur.execute(f"UPDATE Pokemon_cards SET count = count + {soldQuantity} WHERE owner_id IS NULL AND card_name = '{pokemon}'")
            if cur.rowcount == 0:
                #  - QUERY FROM THE POKEMON CARD WE JUST SOLD FOR THE CARD TYPE AND RARITY
                cur.execute(f"SELECT card_type, rarity FROM Pokemon_cards WHERE card_name = '{pokemon}'")
                cardData = cur.fetchall()
                #  - INSERT THE CARD INTO THE POKEMON CARD TABLE WITH NULL OWNERID
                cur.execute(f"INSERT INTO Pokemon_cards (card_name, card_type, rarity, count, owner_id) VALUES ('{pokemon}', {cardData[0][0]}, {cardData[0][1]}, {soldQuantity}, NULL)")
        cur.execute(f"UPDATE Users SET usd_balance = (usd_balance + ({price}*{soldQuantity})) WHERE ID = {userID}")
        con.commit()
        
        #  - GRAB NEW BALANCE
        cur.execute("SELECT * FROM Users WHERE ID = ?", (int(userID),))
        balance = cur.fetchall()
        
        #  - SEND SUCCESS MESSAGE WITH NEW BALANCE
        return f"200 OK|{balance[0][5]}"
    except Exception as e:
        print(f"s: An error occurred: {e}")
        return "500 Internal Server Error"

__all__ = ["Sell"]