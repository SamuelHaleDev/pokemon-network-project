def Lookup(s, MAX_LINE):
    pokemon = input("Search for pokemon on name: ")
    request = f"LOOKUP {pokemon}\n"
    s.sendall(request.encode())
    response = s.recv(MAX_LINE)
    response = response.decode()
    
    if "200" in response:
        print("Pokemon records found:", response.split("|")[1])
    else:
        print("No pokemon records found.")
        return
    
__all__ = ["Lookup"]