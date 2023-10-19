def Login(cur, data, addr):
    print('s: Received', repr(data), 'from', addr)
    #  - GET USERNAME AND PASSWORD
    username = data.decode().split(" ")[1]
    password = data.decode().split(" ")[2].replace("\n", "")
    
    #  - CHECK IF USERNAME AND PASSWORD ARE CORRECT
    cur.execute("SELECT * FROM Users WHERE user_name = ? AND password = ?", (username, password))
    results = cur.fetchall()
    if len(results) == 0:
        server_response = b"s: Error 403: Wrong UserID or Password"
        filler_list = [0,1]
        data = f"{server_response}{filler_list}"
    else:
        #  - SEND USER DATA
        server_response = b"s: 200: OK|"
        user_data = str(results[0]).encode()
        print(user_data)
        data = f"{server_response}{user_data}"
        
    return data
        
__all__ = ["Login"]