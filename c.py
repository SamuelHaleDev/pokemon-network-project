import socket
import queue
import threading
from cmodules.Request import handle_request
from cmodules.Response import handle_response

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
SERVER_PORT = 4988

MAX_LINE = 256 # Maximum number of bytes to receive

# Client socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
s.connect((SERVER_HOST, SERVER_PORT)) # Connect to server address

def main():
    request_queue = queue.Queue()
    response_queue = queue.Queue()
    QUIT = False
    user_input = ""
    request_thread = threading.Thread(target=handle_request, args=(s, request_queue))
    request_thread.start()
    response_thread = threading.Thread(target=handle_response, args=(s, MAX_LINE, response_queue))  
    response_thread.start()
    while not QUIT:
        user = []
        while user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5" and user_input != "6" and user_input != "7" and user_input != "8" and user_input != "9" and user_input != "10" and user_input != "11":
            user_input = menu()
            while (user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5" and user_input != "6" and user_input != "7" and user_input != "8" and user_input != "9" and user_input != "10" and user_input != "11"):
                user_input = input("c: Invalid input. Please enter a number between 1 and 6.")
            if user_input == "1" and user != []:
                buy_route(user, request_queue, response_queue)
            if user_input == "2" and user != []:
                sell_route(user, request_queue, response_queue)
            if user_input == "3" and user != []:
                list_route(user, request_queue, response_queue)
            if user_input == "4" and user != []:
                balance_route(user, request_queue, response_queue)
            if user_input == "10" and user != [] and user[3] == "Root":
                print("c: SERVER SHUT DOWN")
                #   - Send message to server to shut down
                request_queue.put("SHUTDOWN\n")
                response = response_queue.get()
                if "200" in response:
                    QUIT = True
                    request_thread.join()
                    response_thread.join()
                    s.close()
                    print("c: Connection closed.")
                    break
            if user_input == "11":
                print("c: CLIENT SHUT DOWN")
                #  - Check if server is running
                if check_server_status(request_queue, response_queue):
                    try:
                        #   - Send QUIT message to server
                        request_queue.put("QUIT\n")
                        #   - Wait for confirmation message from server
                        data = response_queue.get()
                        if "200" in data:
                            QUIT = True
                            request_thread.join()
                            response_thread.join()
                            s.close()
                            print("c: Connection closed.")
                            break
                        else:
                            print("c: Error closing connection.")
                    except ConnectionAbortedError:
                        pass
            if user_input == "7":
                user = login_route(request_queue, response_queue)
            if user_input == "8" and user != []:
                user = logout_route(user, request_queue, response_queue)
            if user_input == "5" and user != [] and user[3] == "Root":
                who_route(request_queue, response_queue)
            if user_input == "6" and user != []:
                lookup_route(request_queue, response_queue)
            if user_input == "9" and user != []:
                deposit_route(user, request_queue, response_queue)
            if user_input == "10" and user != [] and user[3] != "Root":
                print("c: You do not have permission to shut down the server.")
            if user_input != "11" and user == []:
                print("c: Please login first.")
            user_input = ""

def buy_route(user, request_queue, response_queue):
    global s, MAX_LINE
    from cmodules.Buy import Buy
    Buy(user, s, MAX_LINE, request_queue, response_queue)
    
def sell_route(user, request_queue, response_queue):
    global s, MAX_LINE
    from cmodules.Sell import SELL
    SELL(user, s, MAX_LINE, request_queue, response_queue)
    
def login_route(request_queue, response_queue):
    global s, MAX_LINE
    from cmodules.Login import Login
    return Login(s, MAX_LINE, request_queue, response_queue)

def balance_route(user, request_queue, response_queue):
    global s, MAX_LINE
    from cmodules.Balance import Balance 
    Balance(user, s, MAX_LINE, request_queue, response_queue)
    
def list_route(user, request_queue, response_queue):
    global s, MAX_LINE
    from cmodules.List import List
    List(user, s, MAX_LINE, request_queue, response_queue)  
    
def logout_route(user, request_queue, response_queue):
    global s, MAX_LINE
    from cmodules.Logout import Logout
    return Logout(user, s, MAX_LINE, request_queue, response_queue)

def who_route(request_queue, response_queue):
    global s, MAX_LINE
    from cmodules.Who import Who
    Who(s, MAX_LINE, request_queue, response_queue)
    
def lookup_route(request_queue, response_queue):
    global s, MAX_LINE
    from cmodules.Lookup import Lookup
    Lookup(s, MAX_LINE, request_queue, response_queue)
    
def deposit_route(user, request_queue, response_queue):
    global s, MAX_LINE
    from cmodules.Deposit import Deposit
    Deposit(user, s, MAX_LINE, request_queue, response_queue)

def check_server_status(request_queue, response_queue):
    # Send a message to the server to check if it's still running
    request_queue.put("STATUS\n")
    data = response_queue.get()
    if "SERVER_RUNNING" in data:
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
    print("5. WHO")
    print("6. LOOKUP")
    print("7. LOGIN")
    print("8. LOGOUT")
    print("9. DEPOSIT")
    print("10. SERVER SHUT DOWN")
    print("11. CLIENT SHUT DOWN")
    
    # Prompt user for input
    option = input("c: Enter option: ")
    
    # Return user input
    return option  
            
main()