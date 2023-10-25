def handle_response(s, MAX_LINE):
    while True:
        data = s.recv(MAX_LINE)
        response = data.decode().split("|")[0].strip()
        data = data.decode().split("|")[1].strip()
        
        if "200" in response:
            return data
        elif "400" in response:
            print("c: Error depositing funds.")
        elif "401" in response:
            print("c: Wrong username or password.")
        elif "404" in response:
            print("c: Your search did not match any records.")
        
        