import socket
from typing import List

# Define server address and port
import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description='Client for Pokemon Network Project')

# Add an argument for the server host
parser.add_argument('server_host', type=str, help='The hostname or IP address of the server')

# Parse the command line arguments
#args = parser.parse_args()

# Use the server host from the command line arguments
SERVER_HOST = "localhost"
SERVER_PORT = 4897
QUIT = False
user_input = ""

MAX_LINE = 256 # Maximum number of bytes to receive

# Client socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
s.connect((SERVER_HOST, SERVER_PORT)) # Connect to server address

def buy_route(user):
    global s
    from cmodules.Buy import Buy
    Buy(user, s)
    
def sell_route(user):
    global s
    from cmodules.Sell import SELL
    SELL(user, s)
    
def login_route():
    global s
    from cmodules.Login import Login
    return Login(s)

def check_server_status():
    # Send a message to the server to check if it's still running
    s.sendall(b"STATUS\n")
    data = s.recv(MAX_LINE)
    if data.decode().strip() == "SERVER_RUNNING":
        return True
    else:
        return False

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
    print("7. LOGIN")
    print("8. LOGOUT")
    print("9. WHO")
    print("10. LOOKUP")
    
    # Prompt user for input
    option = input("c: Enter option: ")
    
    # Return user input
    return option  

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

if __name__ == "__main__":
    while not QUIT:
        user = []
        while user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5" and user_input != "6":
            user_input = menu()
            if (user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5" and user_input != "6" and user_input != "7" and user_input != "8" and user_input != "9" and user_input != "10"):
                print("c: Invalid input. Please enter a number between 1 and 6.")
            if user_input == "1" and user != []:
                buy_route(user)
            if user_input == "2" and user != []:
                sell_route(user)
            if user_input == "3" and user != []:
                #  - BUILD CLIENT REQUEST
                print("c: LISTING ALL RECORDS IN POKEMON CARDS TABLE")
                client_request = "LIST"
                owner_id = user[3]
                client_request = client_request + " " + owner_id
                
                #  - SEND AND RECEIVE DATA
                s.sendall(client_request.encode())
                data = s.recv(MAX_LINE)
                if b"200 OK" in data:
                    response = data.decode().split("|")[1].strip()
                    print(response)
            if user_input == "4" and user != []:
                BALANCE()
                #   - Print user's balance
            if user_input == "5" and user != [] and user[3] == "Root":
                print("c: SERVER SHUT DOWN")
                #   - Send message to server to shut down
                s.sendall(b"SHUTDOWN\n")
                data = s.recv(MAX_LINE)
                print("c:", data.decode().strip())
            if user_input == "6" and user != [] and user[3] == "Root":
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
            if user_input == "7":
                user = login_route()
            if user_input == "8" and user != []:
                user = []
                print("c: LOGOUT")
                #  - Code logout functionality in a separate module
            if user_input == "9" and user != []:
                print("c: WHO")
            if user_input == "10" and user != []:
                print("c: LOOKUP")
            user_input = ""