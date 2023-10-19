def List(cur, data, addr):
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
    return f"200 OK|{str(results)}"

__all__ = ["List"]
    