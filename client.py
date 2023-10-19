import socket
from typing import List

# Define server address and port
import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description='Client for Pokemon Network Project')

# Add an argument for the server host
parser.add_argument('server_host', type=str, help='The hostname or IP address of the server')

# Parse the command line arguments
args = parser.parse_args()

# Use the server host from the command line arguments
SERVER_HOST = args.server_host
SERVER_PORT = 4896
QUIT = False
user_input = ""

MAX_LINE = 256 # Maximum number of bytes to receive

# Client socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
s.connect((SERVER_HOST, SERVER_PORT)) # Connect to server address

def check_server_status():
    # Send a message to the server to check if it's still running
    s.sendall(b"STATUS\n")
    data = s.recv(MAX_LINE)
    if data.decode().strip() == "SERVER_RUNNING":
        return True
    else:
        return False

def login():
    # Prompt user for username and password
    username = input("c: Enter username: ")
    password = input("c: Enter password: ")
    # Send "LOGIN" + username + password to server
    s.sendall(("LOGIN " + username + " " + password + "\n").encode())
    # Receive response from server
    data = s.recv(MAX_LINE)
    # data = 'b\'s: 200: Login successful.|\'b"(1, \'John\', \'Doe\', \'j_doe\', \'Passwrd4\', 80.0)"'
    # Parse data to separate user data from login response
    response = data.split(b"|")[0]
    # Check if login was successful by checking if 200 is in data
    if b"200" in response:  
        user_data = data.split(b"|")[1]
        print("c: Login successful.")
        # Turn user_data into a list
        user_data = user_data.decode().replace("b", "").replace("\\", "").replace("(", "").replace(")", "").replace("'", "").replace('"', "")
        user_data = user_data.split(", ")
        # Return user_data
        print(user_data)
        return user_data
    else:
        print("c: Login failed.")
        log = login()
        return log
        

# Write the menu function that prints the options for the user
# Declare the menu function
def menu():
    # Print menu options
    print("1. BUY")
    print("2. SELL")
    print("3. LISTING ALL RECORDS IN POKEMON CARDS TABLE")
    print("4. BALANCE")
    print("5. SERVER SHUT DOWN")
    print("6. CLIENT SHUT DOWN")
    
    # Prompt user for input
    option = input("c: Enter option: ")
    
    # Return user input
    return option

# Log on
user = login()

def Buy():
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
    

def SELL():
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


def BALANCE():
    #User Checks their balance
    userID = user[0]
    money = "BALANCE " + userID
    s.sendall(money.encode())
    money = str(s.recv(MAX_LINE))
    money = money.split("'")[1]
    balance = ""
    for c in money: 
            if c.isdigit() or (c == '.'): 
                balance = balance + c

    print(balance)



while not QUIT:
    while user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5" and user_input != "6":
        user_input = menu()
        if (user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5" and user_input != "6"):
            print("c: Invalid input. Please enter a number between 1 and 6.")
    if user_input == "1":
        Buy()
    if user_input == "2":
        #print("c: SELL")
        SELL()
        #   - Prompt user for card name and quantity
        #   - Check if card exists in table
        #   - Check if user has enough cards
        #   - If all checks pass, update card count and user balance
        #   - If any check fails, print error message
    if user_input == "3":
        #  - BUILD CLIENT REQUEST
        print("c: LISTING ALL RECORDS IN POKEMON CARDS TABLE")
        client_request = "LIST"
        owner_id = user[0]
        if (owner_id == "ROOT"):
            owner_id = input("c: Enter the ID of the user you want to list or type ALL to list all users: ")
        else:
            owner_id = user[0]
        client_request = client_request + " " + owner_id
        
        #  - SEND AND RECEIVE DATA
        s.sendall(client_request.encode())
        data = s.recv(MAX_LINE)
        print(data.decode())
    if user_input == "4":
        BALANCE()
        #   - Print user's balance
    if user_input == "5":
        print("c: SERVER SHUT DOWN")
        #   - Send message to server to shut down
        s.sendall(b"SHUTDOWN\n")
        data = s.recv(MAX_LINE)
        print("c:", data.decode().strip())
    if user_input == "6":
        print("c: CLIENT SHUT DOWN")
        #  - Check if server is running
        if check_server_status():
            try:
                #   - Send QUIT message to server
                s.sendall("QUIT".encode())
                #   - Wait for confirmation message from server
                data = s.recv(MAX_LINE)
                if b"200 OK" in data:
                    QUIT = True
                s.close()
            except ConnectionAbortedError:
                pass
        QUIT = True
    user_input = ""
    

