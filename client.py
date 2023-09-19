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

while not QUIT:
    while user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5" and user_input != "6":
        user_input = menu()
        if (user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5" and user_input != "6"):
            print("c: Invalid input. Please enter a number between 1 and 6.")
        
    # Write a menu that provides the following options:
    # BUY, SELL, LISTING ALL RECORDS IN POKEMON CARDS TABLE, BALANCE, SERVER SHUT DOWN, CLIENT SHUT DOWN
    if user_input == "1":
        print("c: BUY")
        #   - Prompt user for card name and quantity
        #   - Check if card exists in table
        #   - Check if quantity is available
        #   - Check if user has enough money
        #   - If all checks pass, update card count and user balance
        #   - If any check fails, print error message
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

# Send data
s.sendall(b'Hello, world') # Send data to server

# Receive data
data = s.recv(MAX_LINE) # Receive data from server

# Close the connection
s.close()

# Print received data
print('Received', repr(data)) # Print received data
