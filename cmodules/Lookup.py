def Lookup(s, MAX_LINE, request_queue):
    pokemon = input("Search for pokemon on name: ")
    request = f"LOOKUP {pokemon}\n"
    request_queue.put(request)
    response = s.recv(MAX_LINE)
    response = response.decode()
    
    if "200" in response:
        print("Pokemon records found:", response.split("|")[1])
    else:
        print("No pokemon records found.")
        return
    
__all__ = ["Lookup"]