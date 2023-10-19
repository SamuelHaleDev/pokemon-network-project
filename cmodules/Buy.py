from c import MAX_LINE, socket

def Buy(user, s):
    #  - GET CARD DATA
    user_input = input("c: Enter card name: ")
    user_input = "QUERY " + user_input
    s.sendall(user_input.encode())
    data = s.recv(MAX_LINE)
    if b"Error" in data:
        print(data.decode())
        print("c: Card {}".format(user_input.split(" ")[1]))
        return
    pokemon = data.decode().replace("(", "").replace(")", "").replace("'", "").split(", ")
    
    #  - PROMPT USER FOR DESIRED QUANTITY 
    quantity = input("c: Enter quantity: ")
    #  - CHECK IF QUANTITY IS VALID
    if (int(quantity) < 0):
        print("c: Invalid quantity. Please enter a number greater than 0.")
        return
    if (int(quantity) > int(pokemon[4])):
        print("c: Not enough stock.")
        return
    
    #  - PROMPT USER FOR PRICE   
    price = input("c: Enter price: ")
    if (float(price) < 0):
        print("c: Invalid price. Please enter a number greater than 0.")
        return
    #  - CHECK IF USER HAS ENOUGH FUNDS
    if (float(user[5]) < float(price)*int(quantity)):
        print("c: Insufficient funds. Please enter a lower price.")
        return
    #  - SEND REQUEST TO SERVER
    client_request = "BUY {} {} {} {} {} {}".format(pokemon[1], pokemon[2], price, quantity, pokemon[5], user[0])
    s.sendall(client_request.encode())
    data = s.recv(MAX_LINE)
    
    #  - IF 200 IS IN DATA, TRANSACTION SUCCESSFUL
    if b"200" in data:
        balance = data.split(b"|")[1]
        print("c: Bought: {} {} New Balance: {}".format(quantity, pokemon[1], float(balance)))
    else:
        #  - ELSE TRANSACTION FAILED
        print("c: Transaction failed. Server Message: {}".format(data.decode()))
        
__all__ = ["Buy"]