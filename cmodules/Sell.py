from c import MAX_LINE

def SELL(user, s):
    pokemon = input("Please enter the Pokemon you want to sell or type CANCEL to exit:")
    while pokemon == "":
        pokemon = input("Please enter a Pokemon to sell: ")

    userID = user[0]

    inventory_request = "INVENTORY " + pokemon + " " + userID
    s.sendall(inventory_request.encode())
    data = str(s.recv(MAX_LINE))
    ir, data, data2 = data.split("'")
    count = ""

    #quantity = data.split("'")
    #print(data)
    #print(count)
    while (data == "NOTFOUND") and not (pokemon == "CANCEL"):
        print("Pokemon Not Found")
        pokemon = input("Please enter the Pokemon you want to sell or type CANCEL to exit:") 
        #pokemon = "QUERYSELL " + pokemon + " " + userID
        inventory_request = "INVENTORY " + pokemon + " " + userID
        s.sendall(inventory_request.encode())
        data = str(s.recv(MAX_LINE))
        ir, data, data2 = data.split("'")


    for c in data2: 
            if c.isdigit(): 
                count = count + c

    #print(f"You are trying to sell {data}")

    #print(count)

    if pokemon == "CANCEL":
        return

    quantity = input("Please enter the quantity you want to sell: ")
    while quantity == "":
        quantity = input("Please enter a quantity to sell: ")

    #print(trueCount)

    while (int(count) < int(quantity)):
        quantity = input("You do not own that many, how many would you like to sell? ")

    while (int(quantity) < 0):
        quantity = input("Please enter a quantity to sell: ")
        
    price = input("Please enter the price you want to sell for:")
    while (price == "") or (float(price) < 0):
        price = input("Please enter a price to sell(Price must be greater then $0): ")


    sell_request = "SELL " + data + " " + quantity + " " + price + " " + userID
    s.sendall(sell_request.encode())    
    #print(f"SELL {pokemon} {quantity} {price} {ID}")

    data = s.recv(MAX_LINE)
    #cur.execute(f"UPDATE Pokemon_cards SET count = (count - {quantity}) WHERE owner_id = {user_ID} AND card_name = '{pokemon}'")
    #cur.execute(f"UPDATE Users SET usd_balance = (usd_balance + ({price}*{quantity})) WHERE ID = {user_ID}")
    #print(f"Confirming the sale of\tPokemon: {pokemon}\tQuantity: {quantity}\tPrice: {price}")
    
__all__ = ["SELL"]