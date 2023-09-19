import socket

# Define server address and port
SERVER_HOST = 'localhost'
SERVER_PORT = 4895
QUIT = False
user_input = ""

MAX_LINE = 256 # Maximum number of bytes to receive

# Client socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
s.connect((SERVER_HOST, SERVER_PORT)) # Connect to server address

def login():
    # Prompt user for username and password
    username = input("c: Enter username: ")
    password = input("c: Enter password: ")
    # Send "LOGIN" + username + password to server
    s.sendall(("LOGIN " + username + " " + password).encode())
    # Receive response from server
    data = s.recv(MAX_LINE)
    # data = 'b\'s: 200: Login successful.|\'b"(1, \'John\', \'Doe\', \'j_doe\', \'Passwrd4\', 80.0)"'
    # Parse data to separate user data from login response
    user_data = data.split(b"|")[1]
    data = data.split(b"|")[0]
    # Check if login was successful by checking if 200 is in data
    if b"200" in data:
        print("c: Login successful.")
        # Turn user_data into a list
        user_data = user_data.decode().replace("b", "").replace("\\", "").replace("(", "").replace(")", "").replace("'", "").replace('"', "")
        user_data = user_data.split(", ")
        # Return user_data
        return user_data
    else:
        print("c: Login failed.")

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
    print(data.decode())
    pokemon = data.decode().replace("(", "").replace(")", "").replace("'", "").split(", ")
    
    #  - PROMPT USER FOR DESIRED QUANTITY AND PRICE
    quantity = input("c: Enter quantity: ")
    price = input("c: Enter price: ")
    
    #  - CHECK IF ENOUGH CARDS EXIST
    if (int(quantity) > int(pokemon[4])):
        print("c: Insufficient quantity.")
    #  - CHECK IF USER HAS ENOUGH FUNDS
    elif (float(user[5]) < float(price)*int(quantity)):
        print("c: Insufficient funds.")
    #  - CHECK IF USER ALREADY OWNS CARD
    elif (int(user[0]) == int(pokemon[len(pokemon)-1])):
        print("c: You already own this card.")
    else:
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
    
while not QUIT:
    while user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5" and user_input != "6":
        user_input = menu()
        if (user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5" and user_input != "6"):
            print("c: Invalid input. Please enter a number between 1 and 6.")
    if user_input == "1":
        Buy()
    if user_input == "2":
        print("c: SELL")
        #   - Prompt user for card name and quantity
        #   - Check if card exists in table
        #   - Check if user has enough cards
        #   - If all checks pass, update card count and user balance
        #   - If any check fails, print error message
    if user_input == "3":
        print("c: LISTING ALL RECORDS IN POKEMON CARDS TABLE")
        #   - Print all records in Pokemon_cards table
    if user_input == "4":
        print("c: BALANCE")
        #   - Print user's balance
    if user_input == "5":
        print("c: SERVER SHUT DOWN")
        #   - Send message to server to shut down
    if user_input == "6":
        print("c: CLIENT SHUT DOWN")
        #   - Close connection
        #   - Set QUIT to True
        #   - Break out of while loop
    

# Close the connection
s.close()

