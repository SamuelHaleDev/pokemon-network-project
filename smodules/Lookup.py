def Lookup(cur, con, data, addr):
    try:
        print('s: Received LOOKUP command from', addr)
        data = data.decode()
        data = data.split(' ')
        pokemon = data[1]
        pokemon = pokemon.replace('\n', '')
        
        # query database allowing partial matches
        cur.execute("SELECT * FROM Pokemon_cards WHERE card_name LIKE ? OR card_type LIKE ? OR rarity LIKE ? OR count LIKE ?", (pokemon, pokemon, pokemon, pokemon))
        results = cur.fetchall()
        
        # send results back to client
        if len(results) == 0:
            return f"404 ERROR: No cards found"
        else:
            # send back all results
            return f"200 OK|{results}"
    except Exception as e:
        print(f"s: An error occurred: {e}")
        return "500 Internal Server Error"
    
    
    
__all__ = ["Lookup"]