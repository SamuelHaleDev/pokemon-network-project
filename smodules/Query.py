def Query(cur, data, addr):
    print('s: Received', repr(data), 'from', addr)
                
    #  - GET CARD DATA
    card_name = data.decode().split(" ")[1]
    cur.execute("SELECT * FROM Pokemon_cards WHERE card_name = ? AND owner_id IS NULL", (card_name,))
    results = cur.fetchall()
    
    #  - SEND CARD DATA OR ERROR MESSAGE
    if len(results) == 0:
        data = b"s: Error 403: Card does not exist."
    else:
        data = str(results[0])
        
    return data
        
__all__ = ["Query"]