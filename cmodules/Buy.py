import ast

def Buy(user, s, MAX_LINE, request_queue, response_queue):
    try:
        #  - GET CARD DATA
        user_input = input("c: Enter card name: ")
        user_input = "LOOKUP " + user_input
        request_queue.put(user_input)
        data = response_queue.get()
        if "400" in data or "401" in data or "404" in data:
            print(data.decode())
            print("c: Card {}".format(user_input.split(" ")[1]))
            return
        pokemon = ast.literal_eval(data)[0]
        
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
        request_queue.put(client_request)
        data = response_queue.get()
        
        #  - IF 200 IS IN DATA, TRANSACTION SUCCESSFUL
        if "400" in data or "401" in data or "404" in data:
            print("c: Transaction failed. Server Message: {}".format(data))
        else:
            balance = data
            print("c: Bought: {} {} New Balance: {}".format(quantity, pokemon[1], float(balance)))
    except Exception as e:
        print(f"c: An error occurred: {e}")
        print("c: Buy failed.")
        return
        
__all__ = ["Buy"]