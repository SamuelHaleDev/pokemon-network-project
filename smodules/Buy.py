def Buy(cur, addr, con, data):
    #  - GRAB CLIENT REQUEST
    client_request = data.decode().replace("BUY ", "").split(" ")
    print("s: RECEIVED {} FROM ADDRESS {}".format(client_request, addr))
    
    #  - GRAB CARD DATA
    card_name = data.decode().split(" ")[1]
    cur.execute("SELECT * FROM Pokemon_cards WHERE card_name = ?", (card_name,))
    results = cur.fetchall()
    
    #  - CHECK IF CARD EXISTS. IF NOT, SEND ERROR MESSAGE
    if len(results) == 0:
        data = b"s: Error 403: Card does not exist."
    else:
        #  - CHECK IF USER IS BUYING ALL CARDS. IF SO, UPDATE OWNER_ID. 
        if int(client_request[3]) == int(results[0][4]):
            cur.execute("UPDATE Pokemon_cards SET owner_id = ? WHERE card_name = ?", (int(client_request[5]), card_name))
        else:
            #  - IF NOT, UPDATE COUNT AND ADD NEW ROW
            cur.execute("UPDATE Pokemon_cards SET count = count - ? WHERE card_name = ? AND owner_id IS NULL",
                        (int(client_request[3]), card_name))
            #  - UPDATE ROW IF ROW EXISTS
            cur.execute("UPDATE Pokemon_cards SET count = count + ? WHERE card_name = ? AND owner_id = ?",
                        (int(client_request[3]), card_name, int(client_request[5])))
            if cur.rowcount == 0:
                # If user doesn't own the card, insert a new row
                cur.execute("INSERT INTO Pokemon_cards(card_name, card_type, rarity, count, owner_id) VALUES (?, ?, ?, ?, ?)"
                            , (card_name, results[0][2], results[0][3], int(client_request[3]), int(client_request[5])))
        cur.execute("UPDATE Users SET usd_balance = usd_balance - ? WHERE ID = ?", (
            int(client_request[3])*float(client_request[2]), int(client_request[5])))
        con.commit()
        
        #  - GRAB NEW BALANCE
        cur.execute("SELECT * FROM Users WHERE ID = ?", (int(client_request[5]),))
        balance = cur.fetchall()
        
        #  - SEND SUCCESS MESSAGE WITH NEW BALANCE
        return f"200 OK|{balance[0][5]}"
        
__all__ = ["Buy"]