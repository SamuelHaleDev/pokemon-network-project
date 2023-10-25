def SELL(user, s, MAX_LINE, request_queue):
    pokemon = input("Please enter the Pokemon you want to sell or type CANCEL to exit:")
    while pokemon == "":
        pokemon = input("Please enter a Pokemon to sell: ")

    userID = user[0]

    inventory_request = "INVENTORY " + pokemon + " " + userID
    request_queue.put(inventory_request)
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
        request_queue.put(inventory_request)
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
    request_queue.put(sell_request)   
    #print(f"SELL {pokemon} {quantity} {price} {ID}")

    data = s.recv(MAX_LINE)
    
    #  - IF 200 IS IN DATA, TRANSACTION SUCCESSFUL
    if b"200" in data:
        balance = data.split(b"|")[1]
        print("c: Sold: {} {} New Balance: {}".format(quantity, pokemon, float(balance)))
    else:
        #  - ELSE TRANSACTION FAILED
        print("c: Transaction failed. Server Message: {}".format(data.decode()))
    
__all__ = ["SELL"]