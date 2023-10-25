def handle_response(s, MAX_LINE, response_queue):
    while True:
        data = s.recv(MAX_LINE)
        response = data.decode().split("|")[0].strip()
        data = data.decode().split("|")[1].strip()
        
        if "200" in response:
            response_queue.put(data)
        elif "400" in response:
            print("c: Error depositing funds.")
            response_queue.put(response)
        elif "401" in response:
            print("c: Wrong username or password.")
            response_queue.put(response)
        elif "404" in response:
            print("c: Your search did not match any records.")
            response_queue.put(response)
        
        