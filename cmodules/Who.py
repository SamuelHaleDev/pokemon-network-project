def Who(s, MAX_LINE):
    request = f"WHO\n"
    s.sendall(request.encode())
    response = s.recv(MAX_LINE)
    response = response.decode()
    if "200" in response:
        # split the request after '|' character
        response = response.split('|')
        print(f"The list of active users: {response[1]}")
    else:
        print("c: WHO failed.")
    
__all__ = ["Who"]