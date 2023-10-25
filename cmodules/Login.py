def Login(s, MAX_LINE, request_queue, response_queue):
    try:
        # Prompt user for username and password
        username = input("c: Enter username: ")
        password = input("c: Enter password: ")
        # Send "LOGIN" + username + password to server
        request_queue.put(("LOGIN " + username + " " + password + "\n"))
        # data = 'b\'s: 200: Login successful.|\'b"(1, \'John\', \'Doe\', \'j_doe\', \'Passwrd4\', 80.0)"'
        # Parse data to separate user data from login response
        response = response_queue.get()
        # Check if login was successful by checking if 200 is in data
        if "400" in response or "401" in response or "403" in response or "404" in response:  
            log = Login(s, MAX_LINE, request_queue, response_queue)
            return log
        else:
            user_data = response.strip()
            print("c: Login successful.")
            # Turn user_data into a list
            user_data = user_data.replace("b", "").replace("\\", "").replace("(", "").replace(")", "").replace("'", "").replace('"', "")
            user_data = user_data.split(", ")
            return user_data
    except Exception as e:
        print(f"c: An error occurred: {e}")
        print("c: Login failed.")
        return []
    
__all__ = ["Login"]