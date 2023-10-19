from c import MAX_LINE

def Login(s):
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
        log = Login()
        return log
    
__all__ = ["Login"]