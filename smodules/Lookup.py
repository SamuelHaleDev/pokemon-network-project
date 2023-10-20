def Lookup(cur, con, data, addr):
    print('s: Received LOOKUP command from', addr)
    # data will be 'LOOKUP <card_name>'
    # or data could be 'LOOKUP <card_type>' or any other attribute in the card 
    # they can only look up on one attribute at a time though. I.e. they can't lookup on name and type in the same request
    # parse data
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
    
    
    
__all__ = ["Lookup"]